"""Client for Kameleoon"""
import json
import threading
import time
from json import JSONDecodeError
from typing import Callable, Optional, Union, Any, Type, List, Dict, Literal
from urllib.parse import urlencode
import warnings
from dateutil import parser

import requests
from requests import Response
from kameleoon.client_configuration import KameleoonClientConfiguration
from kameleoon.configuration_settings import KameleoonConfigurationSettings

from kameleoon.data import Conversion, get_nonce, Data
from kameleoon.defaults import DEFAULT_BLOCKING, DEFAULT_CONFIGURATION_PATH, DEFAULT_TIMEOUT_MILLISECONDS, \
    DEFAULT_TIMEOUT_SECONDS, DEFAULT_VISITOR_DATA_MAXIMUM_SIZE, DEFAULT_CONFIGURATION_UPDATE_INTERVAL
from kameleoon.helpers.multi_threading import run_in_threads_if_required
from kameleoon.helpers.repeat_timer import RepeatTimer
from kameleoon.real_time.real_time_configuration_service import RealTimeConfigurationService
from kameleoon.storage.varation_storage import VariationStorage
from kameleoon.targeting.tree_condition_factory import ConditionType
from kameleoon.version import __version__ as kameleoon_python_version

from kameleoon.exceptions import \
    ExperimentConfigurationNotFound, NotTargeted, NotActivated, SiteCodeDisabled, VariationConfigurationNotFound,\
    FeatureConfigurationNotFound, FeatureVariableNotFound
from kameleoon.helpers.functions import check_visitor_code, obtain_hash_double, get_size, read_kameleoon_cookie_value
from kameleoon.helpers.logger import get_logger
from kameleoon.helpers.config import config
from kameleoon.targeting.models import Segment

__all__ = ["KameleoonClient", ]

REFERENCE = 0
X_PAGINATION_PAGE_COUNT = "X-Pagination-Page-Count"
SEGMENT = "targetingSegment"
KAMELEOON_TRACK_EXPERIMENT_THREAD = "KameleoonTrackExperimentThread"
KAMELEOON_TRACK_DATA_THREAD = "KameleoonTrackDataThread"
KAMELEOON_ACTIVATE_FEATURE_THREAD = "KameleoonActivateFeatureThread"
STATUS_ACTIVE = "ACTIVE"
FEATURE_STATUS_DEACTIVATED = "DEACTIVATED"


class KameleoonClient:
    """
    KameleoonClient

    Example:

    .. code-block:: python3

        from kameleoon import KameleoonClient

        SITE_CODE = 'a8st4f59bj'

        kameleoon_client = KameleoonClient(SITE_CODE)

        kameleoon_client = KameleoonClient(SITE_CODE, blocking=False,
                           configuration_path='/etc/kameleoon/client-python.yaml')

        kameleoon_client = KameleoonClient(SITE_CODE, blocking=True)

        kameleoon_client = KameleoonClient(SITE_CODE, blocking=True, logger=MyLogger)
    """
    initialize = False
    timer: Optional[threading.Timer] = None

    # pylint: disable=R0913
    def __init__(
            self, site_code: str,
            blocking: bool = DEFAULT_BLOCKING,
            configuration_path: str = DEFAULT_CONFIGURATION_PATH,
            configuration_object: Optional[KameleoonClientConfiguration] = None,
            logger=None
    ):
        """
        :param site_code: Code of the website you want to run experiments on. This unique code id can
                              be found in our platform's back-office. This field is mandatory.
        :type site_code: str

        :param blocking: This parameter defines if the trigger_experiment() method has a non-blocking or
                               blocking behavior. Value true will set it to be blocking.
                               This field is optional and set to False by default.
        :type blocking: bool
        :param configuration_path: Path to the SDK configuration file.
                                   This field is optional and set to /etc/kameleoon/client-python.yaml by default.
        :type configuration_path: str
        :param configuration:   Configuration object which can be used instead of external file at configuration_path.
                                This field is optional set to None by default.
        :type configuration: KameleoonClientConfiguration
        :param logger: Optional component which provides a log method to log messages. By default see method get_logger.
        """
        # pylint: disable=too-many-instance-attributes
        # Eight is reasonable in this case.
        self.site_code = site_code
        self.blocking = blocking
        self.experiments: List[Dict[str, Any]] = []
        self.feature_flags: List[Dict[str, str]] = []
        self.configuration_settings = KameleoonConfigurationSettings()
        self.logger = logger or get_logger()
        self.automation_base_url = "https://api.kameleoon.com/"
        self.client_config_url = "https://client-config.kameleoon.com/"
        self.api_data_url = "https://api-data.kameleoon.com/"
        self.events_url = "https://events.kameleoon.com:8110/"
        self.variation_storage = VariationStorage()
        self.real_time_configuration_service: Optional[RealTimeConfigurationService] = None
        self.update_configuration_handler: Optional[Callable[[], None]] = None
        self._setup_client_configuration(configuration_path, configuration_object)

        self.data: Dict[str, List[Type[Data]]] = {}

        self._init_fetch_configuration()

    def __del__(self):
        self._clear_timer()

    def make_sync_request(self, url: str, headers: Optional[Dict[str, str]] = None,
                          filters: Optional[List[Dict[str, Union[str, List[Union[str, int]]]]]] = None,
                          payload=None,
                          method: Literal['post', 'get'] = 'post',
                          timeout: Optional[float] = DEFAULT_TIMEOUT_SECONDS) -> Optional[Any]:
        """
        :param url: API URL
        :type url: str
        :param headers: request headers
        :type headers: dict
        :param filters: filters
        :type filters: dict
        :param payload: post data or get params dict
        :type payload: any
        :param method: post or get, defaults to post
        :type method: Literal['post', 'get']
        :param timeout: requests timeout
        :type timeout: int
        :return:
        """

        # pylint: disable=too-many-arguments
        if payload is None:
            payload = {}
        if filters:
            payload['filter'] = json.dumps(filters)
        resp_dict: Any = {}
        if method == 'post':
            try:
                resp_dict = requests.post(url, data=payload, headers=headers, timeout=timeout)
            except requests.exceptions.RequestException as ex:
                self.logger.error(ex)
        else:
            try:
                resp_dict = requests.get(url, params=payload, headers=headers, timeout=timeout)
            except requests.exceptions.RequestException as ex:
                self.logger.error(ex)
        if not resp_dict or resp_dict.ok is not True:
            self.logger.error("Failed to fetch %s", resp_dict)
            return None
        try:
            resp = resp_dict.json()
        except JSONDecodeError:
            resp = None
            if isinstance(resp_dict, (Dict, str, Response)):
                resp = resp_dict
        return resp

    def _fetch_all(self,
                   url: str, headers: Dict[str, str],
                   filters=None, payload=None,
                   timeout=DEFAULT_TIMEOUT_SECONDS):
        """
        Getting data from multiple data pages
        :param url: API URL
        :param headers: request headers
        :param filters:
        :param payload: post data or get params dict
        :param timeout: requests timeout
        :return:
        """
        # pylint: disable=too-many-arguments,no-self-use
        if payload is None:
            payload = {}
        if filters:
            payload['filter'] = json.dumps(filters)
        results = []
        current_page = 1
        while True:
            payload['page'] = current_page
            http = None
            try:
                http = requests.get(url, params=payload, headers=headers, timeout=timeout)
            except requests.ConnectionError as ex:
                self.logger.error(ex)
            if not http:
                break
            results += http.json()
            if X_PAGINATION_PAGE_COUNT in http.headers and int(
                    http.headers[X_PAGINATION_PAGE_COUNT]) <= current_page:
                break
            current_page += 1
        return results

    def obtain_visitor_code(self, cookies: Union[str, Dict[str, str]],
                            default_visitor_code: Optional[str] = None) -> str:
        """
        Load cookies from a string (presumably HTTP_COOKIE) or
        from a dictionary.
        See SimpleCookie() https://docs.python.org/3/library/http.cookies.html

        :param cookies: str ot dict
        :param default_visitor_code: Optional str
        :return: kameleoon_cookie_value
        :rtype: str

        Examples:

        .. code-block:: python3

            kameleoon_client = KameleoonClient(SITE_CODE)

            kameleoon_client.obtain_visitor_code(cookies)

            kameleoon_client.obtain_visitor_code(cookies, default_visitor_code)

        """
        # pylint: disable=no-self-use
        return read_kameleoon_cookie_value(cookies, default_visitor_code)

    def trigger_experiment(self, visitor_code: str, experiment_id: int,  # noqa: C901
                           timeout=DEFAULT_TIMEOUT_MILLISECONDS) -> Optional[int]:
        """  Trigger an experiment.

        If such a visitor_code has never been associated with any variation,
        the SDK returns a randomly selected variation.
        If a user with a given visitor_code is already registered with a variation, it will detect the previously
        registered variation and return the variation_id.
        You have to make sure that proper error handling is set up in your code as shown in the example to the right to
        catch potential exceptions.

        :param visitor_code: Visitor code
        :param experiment_id: Id of the experiment you want to trigger.
        :param timeout:
        :return: variation_id:  Id of the variation

        :raises:

            ExperimentConfigurationNotFound: Raise when experiment configuration is not found
            NotActivated: The visitor triggered the experiment, but did not activate it. Usually, this happens because
                          the user has been associated with excluded traffic
            NotTargeted: The visitor is not targeted by the experiment, as the associated targeting segment conditions
                         were not fulfilled. He should see the reference variation
            VisitorCodeNotValid: Raise when the provided visitor code is not valid
                        (empty, or longer than 255 characters)
            SiteCodeDisabled: Raise when the siteCode is not disabled, SDK doesn't work with disabled siteCodes.
                        To make SDK working please enable Site in your account.


        Examples:

        .. code-block:: python

                visitor_code = kameleoon_client.obtain_visitor_code(request.COOKIES)
                variation_id = 0
                try:
                    variation_id = kameleoon_client.trigger_experiment(visitor_code, 135471)
                except NotActivated as ex:
                    variation_id = 0
                    client.logger.error(ex)
                except NotTargeted as ex:
                    variation_id = 0
                    client.logger.error(ex)
                except ExperimentConfigurationNotFound as ex:
                    variation_id = 0
                    client.logger.error(ex)

                recommended_products_number = 5

                if variation_id == 148382:
                    recommended_products_number = 10
                elif variation_id == 187791:
                    recommended_products_number = 8

                response = JsonResponse({...})
                # set a cookie
                response.set_cookie(**kameleoon_cookie)
        """
        # pylint: disable=too-many-locals,no-else-return,no-else-raise
        # pylint: disable=too-many-branches,too-many-statements,too-many-nested-blocks
        check_visitor_code(visitor_code)
        try:
            experiment = [
                experiment for experiment in self.experiments if int(experiment['id']) == int(experiment_id)
            ][0]
        except IndexError as ex:
            raise ExperimentConfigurationNotFound from ex
        if self.blocking:
            timeout = timeout / 1000
            data_not_sent = self._data_not_sent(visitor_code)
            try:
                body: Union[List[str], str] = list(
                    data_instance.obtain_full_post_text_line() for data_instance in  # type: ignore
                    data_not_sent[visitor_code])
            except KeyError:
                body = ''
            path = self._get_experiment_register_url(visitor_code, experiment_id)
            request_options = {"path": path, "body": body}
            self.logger.debug("Trigger experiment request: %s  timeout: %s", request_options, timeout)
            variation_id = self.make_sync_request(f"{self.tracking_base_url}{path}",
                                                  method='post',
                                                  payload=("\n".join(body or '').encode("UTF-8")),
                                                  headers=self._get_header_client(),
                                                  timeout=timeout)
            if not variation_id or isinstance(variation_id, Response):
                self.logger.error("Failed to trigger experiment: %s variation_id %s", experiment_id, variation_id)
                raise ExperimentConfigurationNotFound(message=str(experiment_id))
            elif variation_id in ["null", ""]:
                raise NotTargeted(visitor_code=visitor_code, campaign_key_id=experiment_id)
            elif variation_id == REFERENCE:
                raise NotActivated(visitor_code=visitor_code, campaign_key_id=experiment_id)
            try:
                variation = int(variation_id)
            except (ValueError, TypeError):
                variation = variation_id
            return variation
        else:
            self._check_site_code_enable(experiment)
            if self._check_targeting(visitor_code, experiment):
                variation = 0
                none_variation = True
                saved_variation_id = self._is_valid_saved_variation(
                    visitor_code,
                    experiment_id,
                    experiment['respoolTime'])
                if saved_variation_id is not None:
                    variation = saved_variation_id
                    none_variation = False
                else:
                    threshold = obtain_hash_double(visitor_code, experiment['respoolTime'], experiment['id'])
                    for variation_id, value in experiment['deviations'].items():
                        threshold -= value
                        if threshold < 0:
                            try:
                                variation = int(variation_id)
                            except ValueError:
                                variation = 0
                            none_variation = False
                            self.variation_storage.update_variation(
                                visitor_code=visitor_code,
                                experiment_id=experiment_id,
                                variation_id=variation)
                            break
                api_ssx_parameters = [visitor_code, experiment_id, REFERENCE, none_variation] \
                    if none_variation else [visitor_code, experiment_id, variation]
                run_in_threads_if_required(background_thread=self.multi_threading,
                                           func=self.track_experiment,
                                           args=api_ssx_parameters,
                                           thread_name=KAMELEOON_TRACK_EXPERIMENT_THREAD)
                if none_variation:
                    raise NotActivated(visitor_code=visitor_code, campaign_key_id=experiment_id)
                return variation
            raise NotTargeted(visitor_code=visitor_code, campaign_key_id=experiment_id)

    def _is_valid_saved_variation(self,
                                  visitor_code: str,
                                  experiment_id: int,
                                  respool_times: Dict[str, int]) -> Optional[int]:
        # get saved variation
        saved_variation_id = self.variation_storage.get_variation_id(visitor_code, experiment_id)
        if saved_variation_id is not None:
            # get respool time for saved variation id
            respool_time = respool_times.get(str(saved_variation_id))
            # checking variation for validity along with respoolTime
            return self.variation_storage.is_variation_id_valid(visitor_code, experiment_id, respool_time)
        return None

    def _check_targeting(self, visitor_code: str, campaign: Dict[str, Any]):
        return SEGMENT not in campaign or \
            campaign[SEGMENT] is None or \
            campaign[SEGMENT].check_tree(lambda type: self._get_condition_data(type, visitor_code, campaign['id']))

    def _get_condition_data(self,
                            type_condition_str: str,
                            visitor_code: str,
                            campaign_id: int):
        condition_data: Optional[Any] = None
        condition_type = ConditionType(type_condition_str)
        if condition_type == ConditionType.CUSTOM_DATUM:
            condition_data = self.data[visitor_code] if visitor_code in self.data else []
        if condition_type == ConditionType.TARGET_EXPERIMENT:
            condition_data = self.variation_storage.get_saved_variation_id(visitor_code)
        if condition_type == ConditionType.EXCLUSIVE_EXPERIMENT:
            condition_data = (campaign_id, self.variation_storage.get_saved_variation_id(visitor_code))
        return condition_data

    def _check_data_size(self, visitor_data_maximum_size: int) -> None:
        """
        Checks the memory for exceeding the maximum size
        :param visitor_data_maximum_size: int
        :return: None
        """
        while get_size(self.data) > (visitor_data_maximum_size * (2 ** 20)):
            keys = self.data.keys()
            if len(list(keys)) > 0:
                del self.data[list(keys)[-1]]
            new_data = self.data.copy()
            del self.data
            self.data = new_data
            del new_data
            if get_size({}) >= get_size(self.data):
                break

    def add_data(self, visitor_code: str, *args) -> None:
        """
        To associate various data with the current user, we can use the add_data() method.
        This method requires the visitor_code as a first parameter, and then accepts several additional parameters.
        These additional parameters represent the various Data Types allowed in Kameleoon.

        Note that the add_data() method doesn't return any value and doesn't interact with the Kameleoon back-end
        servers by itself. Instead, all declared data is saved for further sending via the flush() method described
        in the next paragraph. This reduces the number of server calls made, as data is usually grouped
        into a single server call triggered by the execution of flush()

        :param visitor_code: Unique identifier of the user. This field is mandatory.
        :type visitor_code: str
        :param args:
        :return: None

        Examples:

        .. code-block:: python

                from kameleoon.data import PageView

                visitor_code = kameleoon_client.obtain_visitor_code(request.COOKIES)
                kameleoon_client.add_data(visitor_code, CustomData("test-id", "test-value"))
                kameleoon_client.add_data(visitor_code, Browser(BrowserType.CHROME))
                kameleoon_client.add_data(visitor_code, PageView("www.test.com", "test-title"))
                kameleoon_client.add_data(visitor_code, Conversion(1, 100.0))
                kameleoon_client.add_data(visitor_code, Interest(1))
        """
        check_visitor_code(visitor_code)
        try:
            visitor_data_maximum_size = int(self.config['visitor_data_maximum_size'])
        except KeyError:
            visitor_data_maximum_size = DEFAULT_VISITOR_DATA_MAXIMUM_SIZE
        self._check_data_size(visitor_data_maximum_size)
        if args:
            if visitor_code in self.data:
                if not self.data[visitor_code]:
                    self.data[visitor_code] = []
                self.data[visitor_code] += list(args)
            else:
                self.data[visitor_code] = [*args]
        self.logger.debug("Activate feature request")

    def track_conversion(self, visitor_code: str, goal_id: int, revenue: float = 0.0) -> None:
        """
        To track conversion, use the track_conversion() method. This method requires visitor_code and goal_id to track
        conversion on this particular goal. In addition, this method also accepts revenue as a third optional argument
        to track revenue. The visitor_code is usually identical to the one that was used when triggering the experiment.
        The track_conversion() method doesn't return any value. This method is non-blocking as the server
        call is made asynchronously.

        :param visitor_code: Unique identifier of the user. This field is mandatory.
        :type visitor_code: str
        :param goal_id: ID of the goal. This field is mandatory.
        :type goal_id: int
        :param revenue: Revenue of the conversion. This field is optional.
        :type revenue: float
        :return: None
        """
        check_visitor_code(visitor_code)
        self.add_data(visitor_code, Conversion(goal_id, revenue))
        self.flush(visitor_code)

    def flush(self, visitor_code: Optional[str] = None):
        """
        Data associated with the current user via add_data() method is not immediately sent to the server.
        It is stored and accumulated until it is sent automatically by the trigger_experiment()
        or track_conversion() methods, or manually by the flush() method.
        This allows the developer to control exactly when the data is flushed to our servers. For instance,
        if you call the add_data() method a dozen times, it would be a waste of ressources to send data to the
        server after each add_data() invocation. Just call flush() once at the end.
        The flush() method doesn't return any value. This method is non-blocking as the server call
        is made asynchronously.


        :param visitor_code: Unique identifier of the user. This field is mandatory.
        :type visitor_code: Optional[str]

        Examples:

        .. code-block:: python

                from kameleoon.data import PageView

                visitor_code = kameleoon_client.obtain_visitor_code(request.COOKIES)
                kameleoon_client.add_data(visitor_code, CustomData("test-id", "test-value"))
                kameleoon_client.add_data(visitor_code, Browser(BrowserType.CHROME))
                kameleoon_client.add_data(visitor_code, PageView("www.test.com", "test-title"))
                kameleoon_client.add_data(visitor_code, Conversion(1, 100.0))
                kameleoon_client.add_data(visitor_code, Interest(1))

                kameleoon_client.flush()

        """
        if visitor_code is not None:
            check_visitor_code(visitor_code)
        run_in_threads_if_required(background_thread=self.multi_threading,
                                   func=self.track_data,
                                   args=[visitor_code, ],
                                   thread_name=KAMELEOON_TRACK_DATA_THREAD)

    def obtain_variation_associated_data(self, variation_id: int) -> Dict[str, str]:
        """ Obtain variation associated data.

        To retrieve JSON data associated with a variation, call the obtain_variation_associated_data method of our SDK.
        The JSON data usually represents some metadata of the variation, and can be configured on our web application
        interface or via our Automation API.

        This method takes the variationID as a parameter and will return the data as a json string.
        It will throw an exception () if the variation ID is wrong or corresponds to an experiment
        that is not yet online.

        :param variation_id: int  ID of the variation you want to obtain associated data for. This field is mandatory.
        :return: Dict  Data associated with this variationID.

        :raises: VariationNotFound

        Example:

        .. code-block:: python3

                visitor_code = kameleoon_client.obtain_visitor_code(request.COOKIES)

                experiment_id = 75253

                try:
                    variation_id = kameleoon_client.trigger_experiment(visitor_code, experiment_id)
                    dict_object = kameleoon_client.obtain_variation_associated_data(variation_id)
                    first_name = dict_object["firstName"]
                except VariationNotFound:
                    # The variation is not yet activated on Kameleoon's side,
                    ie the associated experiment is not online
                    pass
        """
        variations = list(filter(lambda variation: variation['id'] == variation_id,
                                 [variation
                                 for variations in [experiment['variations'] for experiment in self.experiments]
                                 for variation in variations]))
        if not variations:
            raise VariationConfigurationNotFound(variation_id)
        variation = variations[0]
        return json.loads(variation['customJson'])

    def activate_feature(self, visitor_code: str,
                         feature_key: Union[int, str],
                         timeout=DEFAULT_TIMEOUT_MILLISECONDS) -> bool:
        """
        To activate a feature toggle, call the activate_feature() method of our SDK. This method takes a visitor_code
        and feature_key (or feature_id) as mandatory arguments to check if the specified feature will be active
        for a given user. If such a user has never been associated with this feature flag, the SDK returns a boolean
        value randomly (true if the user should have this feature or false if not). If a user with a given visitor_code
        is already registered with this feature flag, it will detect the previous featureFlag value.
        You have to make sure that proper error handling is set up in your code as shown in the example to the right
        to catch potential exceptions.


        :param visitor_code: str Unique identifier of the user. This field is mandatory.
        :param feature_key: int or str ID of the experiment you want to expose to a user. This field is mandatory.
        :param timeout: int Timeout (in milliseconds). This parameter is only used in the blocking version of
                            this method, and specifies the maximum amount of time the method can block to wait for a
                            result. This field is optional. If not provided,
                            it will use the default value of 2000 milliseconds.
        :return: bool Value of the feature that is registered for a given visitor_code.


        :raises:

            FeatureConfigurationNotFound: Exception indicating that the requested feature ID has not been found in
                                          the internal configuration of the SDK. This is usually normal and means that
                                          the feature flag has not yet been activated on Kameleoon's side
                                          (but code implementing the feature is already deployed on the
                                          web-application's side).
            NotTargeted: Exception indicating that the current visitor / user did not trigger
                         the required targeting conditions for this feature. The targeting conditions are defined
                         via Kameleoon's segment builder.
            VisitorCodeNotValid: Raise when the provided visitor code is not valid
                        (empty, or longer than 255 characters)
            SiteCodeDisabled: Raise when the siteCode is not disabled, SDK doesn't work with disabled siteCodes.
                        To make SDK working please enable Site in your account.

        Examples:

        .. code-block:: python3

                visitor_code = kameleoon_client.obtain_visitor_code(request.COOKIES)
                feature_key = "new_checkout"
                has_new_checkout = False

                try:
                    has_new_checkout = kameleoon_client.activate_feature(visitor_code, feature_key)
                except NotTargeted:
                    # The user did not trigger the feature, as the associated targeting segment conditions were not
                    # fulfilled. The feature should be considered inactive
                    logger.debug(...)
                except FeatureConfigurationNotFound:
                    # The user will not be counted into the experiment, but should see the reference variation
                    logger.debug(...)

                if has_new_checkout:
                    # Implement new checkout code here
        """
        # pylint: disable=no-else-return
        check_visitor_code(visitor_code)
        self._check_feature_key(feature_key)
        feature_flag = self.get_feature_flag(feature_key)
        data_not_sent = self._data_not_sent(visitor_code)
        if self.blocking:
            connexion_options = {"connect_timeout": float(timeout / 1000.0)}
            try:
                body: Union[List[str], str] = [
                    data_instance.obtain_full_post_text_line() for data_instance in  # type: ignore
                    data_not_sent[visitor_code]]
            except KeyError:
                body = ''
            request_options = {
                "path": self._get_experiment_register_url(visitor_code, feature_flag['id']),
                "body": ("\n".join(body).encode("UTF-8")),
                "headers": {"Content-Type": "text/plain"}
            }
            self.logger.debug("Activate feature request: %s", connexion_options)
            self.logger.debug("Activate feature request: %s", request_options)
            resp = self.make_sync_request(f"{self.tracking_base_url}{request_options['path']}",
                                          headers=self._get_header_client(),
                                          payload=request_options['body'],
                                          timeout=connexion_options["connect_timeout"])
            if not resp:
                self.logger.error("Failed to get activation: %s", resp)
                raise FeatureConfigurationNotFound(message=str(feature_flag['id']))
            return resp != "null"
        else:
            self._check_site_code_enable(feature_flag)
            if self._check_targeting(visitor_code, feature_flag):
                if self._feature_flag_scheduled(feature_flag, time.time()):
                    threshold = obtain_hash_double(visitor_code, {}, feature_flag['id'])
                    track_info = []
                    if threshold >= 1 - feature_flag['expositionRate']:
                        variations_id = None
                        if feature_flag["variations"]:
                            variations_id = feature_flag["variations"][0]['id']
                        track_info = [visitor_code, feature_flag['id'], variations_id]
                        activate = True
                    else:
                        track_info = [visitor_code, feature_flag['id'], REFERENCE, True]
                        activate = False
                    run_in_threads_if_required(background_thread=self.multi_threading,
                                               func=self.track_experiment,
                                               args=track_info,
                                               thread_name=KAMELEOON_ACTIVATE_FEATURE_THREAD)
                    return activate
                else:
                    return False
            else:
                raise NotTargeted(visitor_code=visitor_code, campaign_key_id=feature_key)

    # pylint: disable=no-self-use
    def _feature_flag_scheduled(self, feature_flag: Dict[str, Any], date: float) -> bool:
        """
        Checking that feature flag is scheduled then determine its status in current time
        :param feature_flag: Dict[str, Any]
        :return: bool
        """
        current_status = feature_flag['status'] == STATUS_ACTIVE
        if feature_flag['featureStatus'] == FEATURE_STATUS_DEACTIVATED or len(feature_flag['schedules']) == 0:
            return current_status
        for schedule in feature_flag['schedules']:
            if ((schedule.get('dateStart') is None or parser.parse(schedule['dateStart']).timestamp() < date) and
                    (schedule.get('dateEnd') is None or parser.parse(schedule['dateEnd']).timestamp() > date)):
                return True
        return False

    def obtain_feature_variable(self, feature_key: Union[str, int],
                                variable_key: str) -> Union[bool, str, float, Dict[str, Any]]:
        """
        Retrieve a feature variable.
        A feature variable can be changed easily via our web application.

        :param feature_key: Union[str, int] ID or Key of the feature you want to obtain to a user.
                            This field is mandatory.
        :param variable_key: str  Key of the variable. This field is mandatory.
        :return: bool or str or float or dict

        :raises: FeatureVariableNotFound: Exception indicating that the requested variable has not been found.
                                         Check that the variable's ID (or key) matches the one in your code.
                 FeatureConfigurationNotFound: Exception indicating that the requested feature ID has not been found
                                               in the internal configuration of the SDK. This is usually normal and
                                               means that the feature flag has not yet been activated on
                                               Kameleoon's side.

        Example:

        .. code-block:: python3

                feature_key = "myFeature"
                variable_key = "myVariable"
                try:
                    data = kameleoon_client.obtain_feature_variable(feature_key, variable_key)
                except FeatureConfigurationNotFound:
                    # The feature is not yet activated on Kameleoon's side
                    pass
                except FeatureVariableNotFound:
                    # Request variable not defined on Kameleoon's side
                    pass
        """

        # pylint: disable=no-else-raise
        self._check_feature_key(feature_key)
        feature_flag = self.get_feature_flag(feature_key)
        custom_json = None
        try:
            custom_json = json.loads(feature_flag["variations"][0]['customJson'])[variable_key]
        except (IndexError, KeyError) as ex:
            self.logger.error(ex)
            raise FeatureVariableNotFound(variable_key) from ex
        if not custom_json:
            raise FeatureVariableNotFound(variable_key)
        return self._parse_json(custom_json)

    def obtain_feature_all_variables(self, feature_key: str) -> Dict[str, Any]:
        """
        Retrieve all feature variables.
        A feature variables can be changed easily via our web application.

        :param feature_key: str Key of the feature you want to obtain to a user.
                            This field is mandatory.
        :return: Dictionary of feature variables
        :rtype: Dict[str, Any]

        :raises: FeatureConfigurationNotFound: Exception indicating that the requested feature Key has not been found
                                               in the internal configuration of the SDK. This is usually normal and
                                               means that the feature flag has not yet been activated on
                                               Kameleoon's side.

        Example:

        .. code-block:: python3
                try:
                    data = kameleoon_client.obtain_feature_all_variables(feature_key)
                except FeatureConfigurationNotFound:
                    # The feature is not yet activated on Kameleoon's side
                    pass
        """

        # pylint: disable=no-else-raise
        feature_flag = self.get_feature_flag(feature_key)
        all_variables: Dict[str, Any] = {}
        try:
            custom_json = json.loads(feature_flag["variations"][0]['customJson'])
        except (IndexError, KeyError) as ex:
            self.logger.error(ex)
            return all_variables
        for key, value in custom_json.items():
            all_variables[key] = self._parse_json(custom_json=value)
        return all_variables

    def _parse_json(self, custom_json: Dict[str, Any]):
        if custom_json['type'] == 'Boolean':
            return bool(custom_json['value'])
        if custom_json['type'] == 'String':
            return str(custom_json['value'])
        if custom_json['type'] == 'Number':
            return float(custom_json['value'])
        if custom_json['type'] == 'JSON':
            return json.loads(custom_json['value'])
        raise TypeError("Unknown type for feature variable")

    def retrieve_data_from_remote_source(self,
                                         key: str,
                                         timeout: Optional[float] = DEFAULT_TIMEOUT_SECONDS) -> Optional[Any]:
        """
        The retrieved_data_from_remote_source method allows you to retrieve data (according to a key passed as
        argument)stored on a remote Kameleoon server. Usually data will be stored on our remote servers
        via the use of our Data API. This method, along with the availability of our highly scalable servers
        for this purpose, provides a convenient way to quickly store massive amounts of data that
        can be later retrieved for each of your visitors / users.

        :param key: key you want to retrieve data. This field is mandatory.
        :type key: str
        :param timeout: requests timeout (default value is 2000 milliseconds)
        :type timeout: int

        :return: data assosiated with this key, decoded into json
        :rtype: Optional[Any]

        :raises:

            RequestException: All new network exceptions (timeout / connection refused and etc)
            JSONDecodeError: Exceptions happen during JSON decoding
        """
        return self.make_sync_request(
            url=self._get_api_data_request_url(key),
            method='get',
            headers=self._get_header_client(),
            timeout=timeout)

    def obtain_experiment_list(
            self,
            visitor_code: Optional[str] = None,
            only_active: bool = True) -> List[int]:
        """
        The obtain_experiment_list method uses for obtaining a list of experiment IDs:
        - currently available for the SDK
        - currently available for a visitor
        - currently available and active simultaneously for a visitor

        :param visitor_code: unique identifier of a visitor
        :type visitor_code: Optional[str]
        :param only_active: if `onlyActive` parameter is `true` result contains only active experiments,
                            otherwise it contains all targeted experiments for specific `visitorCode`
        :type only_active: bool

        :return: List of all experiments IDs (or targeted, or targeted and active simultaneously)
                 for current visitorCode
        :rtype: List[int]
        """
        # pylint: disable=no-else-return
        if visitor_code:
            return self._obtain_campaign_list(
                visitor_code=visitor_code,
                only_active=only_active,
                is_feature_flag=False)
        else:
            return self._obtain_campaign_list_all(is_feature_flag=False)

    def obtain_feature_list(
            self,
            visitor_code: Optional[str] = None,
            only_active: bool = True) -> List[int]:
        """
        The obtain_feature_list method uses for obtaining a list of feature flag IDs:
        - currently available for the SDK
        - currently available for a visitor
        - currently available and active simultaneously for a visitor

        :param visitor_code: unique identifier of a visitor
        :type visitor_code: Optional[str]
        :param only_active: if `onlyActive` parameter is `true` result contains only active feature flags,
                            otherwise it contains all targeted feature flag for specific `visitorCode`
        :type only_active: bool

        :return: List of all feature flag IDs (or targeted, or targeted and active simultaneously)
                 for current visitorCode
        :rtype: List[int]
        """
        # pylint: disable=no-else-return
        if visitor_code:
            return self._obtain_campaign_list(
                visitor_code=visitor_code,
                only_active=only_active,
                is_feature_flag=True)
        else:
            return self._obtain_campaign_list_all(is_feature_flag=True)

    def _obtain_campaign_list_all(self, is_feature_flag: bool) -> List[int]:
        """
        The _obtain_campaign_list_all method uses for obtaining a list of all
        campaign IDs available for the SDK

        :param is_feature_flag: feature flag or experiment campaign
        :type is_feature_flag: bool

        :return: List of all campaing IDs available for the SDK
        :rtype: List[int]
        """
        list_campaings = self.feature_flags if is_feature_flag else self.experiments
        return list(map(lambda campaign: campaign['id'], list_campaings))

    def _obtain_campaign_list(
            self,
            visitor_code: str,
            only_active: bool,
            is_feature_flag: bool) -> List[int]:
        """
        The _obtain_campaign_list method uses for obtaining a list of campaign IDs:
        - currently available for a visitor
        - currently available and active simultaneously for a visitor

        :param visitor_code: unique identifier of a visitor
        :type visitor_code: Optional[str]
        :param only_active: if `onlyActive` parameter is `true` result contains only active experiments,
                            otherwise it contains all targeted experiments for specific `visitorCode`
        :type only_active: bool

        :return: List of targeted campaign IDs (or targeted and active simultaneously)
                 for current visitorCode
        :rtype: List[int]
        """
        list_result = []
        list_campaings = self.feature_flags if is_feature_flag else self.experiments
        for campaign in list_campaings:
            if self._check_targeting(visitor_code, campaign):
                if only_active:
                    hash_double = obtain_hash_double(visitor_code, {}, campaign['id'])
                    origin_deviation = 1 - campaign['expositionRate'] if is_feature_flag \
                        else campaign['deviations']['origin']
                    if hash_double < origin_deviation:
                        continue
                list_result.append(campaign['id'])
        return list_result

    def _init_fetch_configuration(self) -> None:
        """
        :return:
        """
        self._fetch_configuration()

    def _fetch_configuration(self, time_stamp: Optional[int] = None) -> None:
        """
        fetch configuration from CDN service
        :return:  None
        """
        # pylint: disable=W0703
        try:
            configuration_json = self.obtain_configuration(self.site_code, time_stamp)
            if configuration_json:
                self.experiments = self.fetch_experiments(configuration_json)
                self.feature_flags = self.fetch_feature_flags(configuration_json)
                self.configuration_settings = self._fetch_settings(configuration_json)
                self._call_update_handler_if_needed(time_stamp is not None)
        except Exception as ex:
            self.logger.error(ex)
        self._manage_configuration_update(self.configuration_settings.real_time_update)

    def _call_update_handler_if_needed(self, need_call: bool) -> None:
        """
        Call the handler when configuraiton was updated with new time stamp
        :param need_call: this parameters indicates if we need to call handler or not
        :type need_call: bool
        :return:  None
        """
        if need_call and self.update_configuration_handler is not None:
            self.update_configuration_handler()

    def _manage_configuration_update(self, is_real_time_update: bool):
        if is_real_time_update:
            if self.timer is not None:
                self._clear_timer()
            if self.real_time_configuration_service is None:
                self.real_time_configuration_service = RealTimeConfigurationService(
                    self._get_events_request_url(self.site_code),
                    lambda real_time_event: self._fetch_configuration(real_time_event.time_stamp),
                    logger=self.logger
                )
        else:
            if self.real_time_configuration_service is not None:
                self.real_time_configuration_service.close()
                self.real_time_configuration_service = None
            self._add_fetch_configuration_timer()

    def on_update_configuration(self, handler: Callable[[], None]):
        """
        The `on_update_configuration()` method allows you to handle the event when configuration
        has updated data. It takes one input parameter: callable **handler**. The handler
        that will be called when the configuration is updated using a real-time configuration event.
        :param handler: The handler that will be called when the configuration
        is updated using a real-time configuration event.
        :type need_call: Callable[[None], None]
        :return:  None
        """
        self.update_configuration_handler = handler

    def _add_fetch_configuration_timer(self) -> None:
        """
        Add timer for updating configuration with specific interval (polling mode)
        :return: None
        """
        if self.timer is None:
            self.timer = RepeatTimer(self.actions_configuration_refresh_interval, self._fetch_configuration)
            self.timer.setDaemon(True)
            self.timer.start()

    def _clear_timer(self) -> None:
        """
        Remove timer which updates configuration with specific interval (polling mode)
        :return: None
        """
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

    def _get_header_client(self) -> Dict[str, str]:
        return {
            'Kameleoon-Client': f'sdk/python/{kameleoon_python_version}'
        }

    def _get_filter(self, field: str,
                    operator: str,
                    parameters: List[Union[str, int]]
                    ) -> Dict[str, Union[str, List[Union[str, int]]]]:
        """
        Filters for request
        :param field:
        :param operator:
        :param parameters:
        :return:
        """
        # pylint: disable=no-self-use
        return {'field': field, 'operator': operator, 'parameters': parameters}

    def obtain_configuration(
            self,
            site_code: str,
            time_stamp: Optional[int]) -> Optional[Dict[str, Any]]:
        """
        Obtaining configuration from CDN service
        :param sitecode:
        :type: str
        :return: None
        """
        self.logger.debug('Obtaining configuration')
        url = f"{self.client_config_url}mobile?siteCode={site_code}"
        url += f"&environment={self.environment}" if self.environment else ""
        url += f"&ts={str(time_stamp)}" if time_stamp else ""
        resp = self.make_sync_request(url, method='get')
        return resp

    # fetching segment for both types: experiments and feature_flags (campaigns)
    # pylint: disable=no-self-use
    def _complete_campaign(self, campaign) -> Dict[str, Any]:
        """
        :param campaign (experiment or feature_flag):
        :type: dict
        :return: campaign (experiment or feature_flag)
        :rtype: dict
        """
        campaign['id'] = int(campaign['id'])
        campaign['status'] = campaign['status']
        if 'respoolTime' in campaign and campaign['respoolTime'] is not None:
            campaign['respoolTime'] = {
                ('origin' if respoolTime['variationId'] == "0" else respoolTime['variationId']):
                respoolTime['value'] for respoolTime in campaign['respoolTime']}
        if 'variations' in campaign and campaign['variations'] is not None:
            campaign['variations'] = [{'id': int(variation['id']), 'customJson': variation['customJson']}
                                      for variation in campaign['variations']]
        if 'segment' in campaign and campaign['segment'] is not None:
            campaign['targetingSegment'] = Segment(campaign['segment'])
        return campaign

    def _complete_experiment(self, experiment) -> Dict[str, Any]:
        """
        :param experiment:
        :type: dict
        :return:  experiment
        :rtype: dict
        """
        if 'deviations' in experiment and experiment['deviations'] is not None:
            experiment['deviations'] = {
                ('origin' if deviation['variationId'] == "0" else deviation['variationId']):
                deviation['value'] for deviation in experiment['deviations']}
        return self._complete_campaign(experiment)

    def fetch_experiments(self, configuration: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Fethcing experiments from CDN response
        :param configuration: Full configuration of experiments and feature flags
        :type: Optional[Dict[str, Any]]
        :return: List of experiments
        :rtype: List[Dict[str, Any]]
        """
        experiments = configuration['experiments'] if configuration is not None else []
        if experiments:
            experiments = [self._complete_experiment(experiment) for experiment in experiments]
            self.logger.debug("Experiment are fetched: %s", experiments)
        return experiments

    def fetch_feature_flags(self, configuration: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Fethcing feature flags from CDN response
        :param configuration: Full configuration of experiments and feature flags
        :type: Optional[Dict[str, Any]]
        :return: List of feature flags
        :rtype: List[Dict[str, Any]]
        """
        feature_flags = configuration['featureFlags'] if configuration is not None else []
        if feature_flags:
            feature_flags = [self._complete_campaign(feature_flag) for feature_flag in feature_flags]
            self.logger.debug("Feature Flags are fetched: %s", feature_flags)
        return feature_flags

    def _fetch_settings(self, configuration: Optional[Dict[str, Any]]) -> KameleoonConfigurationSettings:
        """
        Fethcing configuration settings from CDN response
        :param configuration: Full configuration of experiments and feature flags
        :type: Optional[Dict[str, Any]]
        :return: Settings of configuration
        :rtype: Dict[str, Any]
        """
        if configuration:
            settings = KameleoonConfigurationSettings(configuration.get('configuration'))
            return settings
        return self.configuration_settings

    def _get_common_ssx_parameters(self, visitor_code: str) -> Dict[str, str]:
        """
        :param visitor_code:
        :return:
        """
        return {
            'nonce': get_nonce(),
            'siteCode': self.site_code,
            'visitorCode': visitor_code
        }

    def _get_experiment_register_url(self, visitor_code: str, experiment_id: int,
                                     variation_id: Optional[int] = None, none_variation=False) -> str:
        """
        :param visitor_code:
        :param experiment_id:
        :param variation_id:
        :param none_variation:
        :return:
        """
        ssx_parameters = urlencode(self._get_common_ssx_parameters(visitor_code))
        url = f"experimentTracking?{ssx_parameters}&experimentId={experiment_id}"
        if variation_id is not None:
            url += f"&variationId={variation_id}"
        if none_variation:
            url += "&noneVariation=true"
        return url

    def _get_data_register_url(self, visitor_code) -> str:
        """
        Return configured url for API SSX
        :param visitor_code:
        :return:
        """
        return "dataTracking?" + urlencode(self._get_common_ssx_parameters(visitor_code))

    def _get_api_data_request_url(self, key: str) -> str:
        """
        Return configured url for API Data
        :param key:
        :return:
        """
        params = {
            'siteCode': self.site_code,
            'key': key
        }
        return self.api_data_url + "data?" + urlencode(params)

    def _get_events_request_url(self, site_code: str) -> str:
        """
        Return configured url for Real Time configuration service (SSE client)
        :param site_code: site code you're subscribing for real time updates
        :type: str
        :return:
        """
        return self.events_url + "sse?siteCode=" + site_code

    def get_feature_flag(self, feature_key: Union[int, str]) -> Dict[str, Any]:
        """

        :param feature_key:
        :return:
        """
        if isinstance(feature_key, str):
            _id = 'identificationKey'
        elif isinstance(feature_key, int):
            _id = 'id'
        else:
            raise TypeError("Feature key should be a String or an Integer.")
        feature_flags = [feature_flag for feature_flag in self.feature_flags if feature_flag[_id] == feature_key]
        feature_flag = None
        if feature_flags:
            feature_flag = feature_flags[0]
        if feature_flag is None:
            raise FeatureConfigurationNotFound(message=str(feature_key))
        return feature_flag

    def track_experiment(self, visitor_code: str, experiment_id, variation_id=None, none_variation=False) -> None:
        """
        Track experiment
        :param visitor_code:
        :param experiment_id:
        :param variation_id:
        :param none_variation:
        :return: None
        """
        data_not_sent = self._data_not_sent(visitor_code)
        data = data_not_sent.get(visitor_code, [])

        options = {
            "path": self._get_experiment_register_url(visitor_code, experiment_id, variation_id, none_variation),
            "body": ("\n".join([
                data_instance.obtain_full_post_text_line() for data_instance in data]) or "").encode(  # type: ignore
                "UTF-8")
        }
        trial = 0
        self.logger.debug("Start post tracking experiment: %s", data_not_sent)
        success = False
        while trial < 10:
            resp = self.make_sync_request(f"{self.tracking_base_url}{options['path']}",
                                          headers=self._get_header_client(), payload=options['body'])
            self.logger.debug("Request %s", resp)
            if resp:
                for data_instance in data:
                    data_instance.sent = True
                trial += 1
                success = True
                break
            trial += 1
        if success:
            self.logger.debug("Post to experiment tracking is done after %s trials", trial)
        else:
            self.logger.error("Post to experiment tracking is not done after %s trials", trial)

    def track_data(self, visitor_code: Optional[str] = None):
        """
        Tracking data
        :param visitor_code: Optional[str]
        :return:
        """
        trials = 10
        data_not_sent = self._data_not_sent(visitor_code)

        self.logger.debug("Start post tracking data: %s", data_not_sent)

        while trials > 0 and data_not_sent:
            for v_code, data_list_instances in data_not_sent.items():
                body = [data_instance.obtain_full_post_text_line() for data_instance in  # type: ignore
                        data_list_instances]
                options = {
                    'path': self._get_data_register_url(v_code),
                    'body': ("\n".join(body)).encode(
                        "UTF-8")
                }
                self.logger.debug("Post tracking data for visitor_code: %s with options: %s", data_list_instances,
                                  options)
                resp = self.make_sync_request(f"{self.tracking_base_url}{options['path']}",
                                              headers=self._get_header_client(), payload=options['body'])
                if resp:
                    for data_instance in data_list_instances:
                        data_instance.sent = True
                    data_not_sent = self._data_not_sent(visitor_code)
                    if not data_not_sent:
                        break
                trials -= 1
        self.logger.debug("Post to data tracking is done")

    def _data_not_sent(self, visitor_code: Optional[str] = None) -> Dict[str, List[Type[Data]]]:
        """
        :param visitor_code: Optional[str]
        :return: Dict[str, List[Type[Data]]]
        """
        data = {}
        if visitor_code:
            try:
                data[visitor_code] = [
                    data_instance
                    for data_instance in self.data[visitor_code] if not data_instance.sent
                ]
                if not data[visitor_code]:
                    data = {}
            except (KeyError, IndexError) as ex:
                self.logger.error(ex)
        else:
            for vis_code, data_list in self.data.items():
                if data_list:
                    data[vis_code] = [data_instance for data_instance in data_list if not data_instance.sent]
        return data

    def _check_site_code_enable(self, exp_or_ff: Dict[str, Any]):
        """
        raise SiteCodeDisabled if site of Experiment or Feature Flag is disabled
        :param exp_or_ff:
        :type exp_or_ff: Dict[str, Any]
        """
        if exp_or_ff.get('siteEnabled') is not True:
            raise SiteCodeDisabled(self.site_code)

    def _check_feature_key(self, feature_key: Union[str, int]):
        """
        warning user that feature_id is deprecated and need to pass feature_key with `str` type
        :param feature_key:
        :type feature_key: Union[str, int]
        """
        if isinstance(feature_key, int):
            warnings.warn(
                'Passing `feature_key` with type of `int` to `activate_feature` or `obtain_feature_variable` '
                'is deprecated, it will be removed in next releases. This is necessary to support multi-environment '
                'feature')

    def _setup_client_configuration(self,
                                    configuration_path: str,
                                    configuration_object: Optional[KameleoonClientConfiguration]):
        """
        helper method to parse client configuration and setup client
        """
        config_yml = configuration_path or DEFAULT_CONFIGURATION_PATH
        self.config = config(config_yml, configuration_object)
        try:
            target_environment = self.config['target_environment']
        except KeyError:
            target_environment = 'prod'
        if target_environment == 'test':
            self.tracking_base_url = "https://api-ssx.kameleoon.net/"
        else:
            self.tracking_base_url = "https://api-ssx.kameleoon.com/"
        try:
            self.environment = self.config['environment']
        except KeyError:
            self.environment = 'production'
        try:
            self.multi_threading = self.config['multi_threading']
        except KeyError:
            self.multi_threading = False
        try:
            actions_configuration_refresh_interval = int(self.config['actions_configuration_refresh_interval'])
            self.actions_configuration_refresh_interval = actions_configuration_refresh_interval * 60
        except KeyError:
            self.actions_configuration_refresh_interval = DEFAULT_CONFIGURATION_UPDATE_INTERVAL
