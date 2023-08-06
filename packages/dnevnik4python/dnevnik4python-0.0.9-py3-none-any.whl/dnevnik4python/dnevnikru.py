from bs4 import BeautifulSoup
import requests
from requests import Session
from fake_useragent import UserAgent
from os import getenv
from json import loads as json_loads
from datetime import datetime, timedelta
import pytz
import logging
import pprint

from .exceptions import *

logger = logging.getLogger(__name__)

# disable warnings from urllib about lack of SSL cert
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class DiaryBase:
    """Base Dairy class"""

    base_address      =  "xn--b1addnkoc.xn--p1ai"
    base_url          = f"https://{base_address}/"
    login_url         = f"https://login.{base_address}/login/"
    old_login_url     =  "https://login.dnevnik.ru/login/"
    userfeed_url      = f"{base_url}userfeed/"
    api_url           = f"{base_url}api/"

    def __init__(self):
        self._initial_info = None

        self.session = Session()
        # "Referer" is needed
        self.session.headers = {"User-Agent": UserAgent().random,
                                "Referer": "https://login.dnevnik.ru/"}

    def _check_response(func):
        def inner(*args, **kwargs):
            # args[0] is self
            # args[1] is second argument, url in our case
            logger.debug(f"Sending {func.__name__.upper()[1:]} request to {args[1]}")
            logger.debug(f"Session headers (also included in the request): {args[0].session.headers}")

            r = func(*args, **kwargs)

            if r.status_code not in (302, 200):
                logger.error(f"Got {r.status_code} from {args[1]}")
                if not args[0].servers_are_ok():
                    raise ServersAreDownException("Dnevnik.ru servers are down, please retry later")
                else:
                    raise NotOkCodeReturn(f"Get request to {args[1]} resulted in {r.status_code} status code")

            logger.debug(f"Request to {args[1]} sucsessful")
            return r
        return inner

    # simple wrappers for "get" and "post" methods from requests library
    # 
    # we also ignore redirects by default since dnevnik.ru sends fucked up
    # "Location" header with wrong encoding (https://Ð´Ð½ÐµÐ²Ð½Ð¸Ðº.Ñ�Ñ�/ instead of https://дневник.рф/)
    # which breaks "requests" internal redirection code and throws an exception
    @_check_response
    def _get(self, *args, allow_redirects=False, **kwargs): return self.session.get(*args, **kwargs, allow_redirects=allow_redirects)

    @_check_response
    def _post(self, *args, allow_redirects=False, **kwargs): return self.session.post(*args, **kwargs, allow_redirects=allow_redirects)

    def servers_are_ok(self):
        logger.info(f"Checking {self.base_url} status")
        r = self.session.get(f"{self.base_url}")
        if r.status_code != 200:
            logger.warn(f"Unable to reach dnevnik.ru servers [{r.status_code} response code]")
            return False
        logger.info(f"dnevnik.ru server are up")
        return True

    def auth(self, login, password):
        logger.info(f"Authenticating on {self.login_url}")

        r = self._post(self.old_login_url, data={
                                       "login": login,
                                       "password": password}, verify=False)

        # dnevnik.ru redirects to a URL which is used to accsess userfeed
        # however, this URL has a fucked-up encoding and cant be understood by "requests"
        # so we redirect everythin manually (including this)
        token = str(str(r.headers["Location"].split("token=")[1]).split("&returnUrl")[0])
        self._get(f"{self.login_url}token?token={token}&returnUrl=https://дневник.рф/", verify=False)

        # redirect to userfeed
        r = self._get(self.userfeed_url, verify=False)

        # check if we accessed userfeed page
        if r.url != self.userfeed_url:
            logger.error("Unable to authenticate")
            # check for popup that tells you about wrong credentials
            soup = BeautifulSoup(r.text, "lxml")
            msg = soup.find("div", {"class", "login__body__hint"})
            if msg != None:
                raise IncorrectLoginDataException(f"Unable to authenticate. Reason: {msg.text.strip()}")

            raise UnknownLoginError("Unable to authenticate. "
            "Exact reason is unknow, but most likely its due to wrong credentials")

        logger.info("Authenication sucsessful")

    def parse_initial_data(self):
        """
        Parses essential data about from userfeed

        This includes user data: schoolId, groupId, personId 
        And also other info about user, marks, periods, class,
        teachers and much more
        
        I recomend you explore it yourself since this data comes
        directly from dnevnik.ru and can change over time 
        """
        logger.debug("Parsing initial info")
        r = self._get(self.userfeed_url)

        if r.status_code != 200 or r.url != self.userfeed_url:
            raise DataParseError("Cant reach userfeed")

        # there is a JS script on this page that contains all of the info we need
        # we can just parse it
        soup = BeautifulSoup(r.text, "lxml")
        try:
            for script in soup.findAll("script"):
                if "window.__TALK__INITIAL__STATE__" not in script.next:
                    continue
                logger.debug("Found nescessary html tag")
                # remove everything we dont need
                raw_initial_info = script.next
                raw_initial_info = raw_initial_info.split("window.__USER__START__PAGE__INITIAL__STATE__ = ")[1]
                raw_initial_info = raw_initial_info.split("window.__TALK__STUB__INITIAL__STATE__ = ")[0]
                raw_initial_info = raw_initial_info.split("window.__TALK__INITIAL__STATE__ = ")[0]
                raw_initial_info = raw_initial_info.strip()[:-1]
                self._initial_info = json_loads(raw_initial_info)
                info = self._initial_info["userSchedule"]["currentChild"]

                logger.debug("User info according _initial_info: " + str(info))
                logger.debug("Current date according to dnevnik: " + self._initial_info["userSchedule"]["currentDate"])

                return info["schoolId"], info["groupId"], info["personId"]

        except Exception as e:
            logger.error(f"During user info parsing this exception accured:\n{e}")

        raise DataParseError("Cannot find user info in userfeed page")

    @property
    def initial_info(self):
        return self._initial_info


class Diary(DiaryBase):
    """Main Diary class"""

    def __init__(self, login, password):
        super().__init__()

        self.auth(login, password)
        # parse data about user
        self.school_id, self.group_id, self.person_id = self.parse_initial_data()

    def _get_diary(self, date: datetime, span: int):
        # calculate time if user passes in negative span
        # by default dnevnikru supports only positive and zero span
        if span < 0:
            span = abs(span)
            date = date - timedelta(days=span)

        # convert date to UNIX timestamp
        timestamp_date = int(datetime(year=date.year, month=date.month, day=date.day).replace(tzinfo=pytz.utc).timestamp())

        logger.info(f"Getting diary for date {date} ({timestamp_date}) with span {span}")

        # send request directly to dnevnik.ru API
        r = self._get(f"{self.api_url}userfeed/persons/"
                      f"{self.person_id}/schools/"
                      f"{self.school_id}/groups/"
                      f"{self.group_id}/schedule?"
                      f"date={timestamp_date}&amp;"
                      f"takeDays={span}", verify=False)
        return json_loads(r.text)

    def get_diary(self, date: datetime, *args):
        """
        Get a diary for certain date(s)

        Dairy data includes: lesson, their schedule, marks, homeworks,
        basic info about subject and much, much more.

        I recomend you explore it yourself since this data comes
        directly from dnevnik.ru and can change over time 
        """
        if not args:
            return self._get_diary(date, 1)

        arg = args[0]

        if isinstance(arg, int):
            return self._get_diary(date, arg)
        elif isinstance(arg, datetime):
            return self._get_diary(date, arg.day - date.day)
        else:
            raise TypeError(f"Second argument must be datetime or int, not {type(arg)}")

    def get_period_marks(self, period: int):
        """
        Parse marks in a certain period defined
        by dnevnik.ru (most likely - a quater of a year)
        """
        # this method pasrses https://schools.dnevnik.ru/marks.aspx?
        # and takes info about marks
        logger.info("Getting period marks")
        logger.debug("Period info according to _initial_info:\n"
        f"{pprint.pformat(self._initial_info['userContext']['currentContextPerson']['reportingPeriodGroup'])}")

        # these 2 headers are essential
        self.session.headers["Host"] = f"schools.{self.base_address}"
        self.session.headers["Referer"] = self.base_url
        r = self._get(f"https://schools.{self.base_address}/marks.aspx?"
                      f"school={self.school_id}&"
                      # i have no idea what this is
                      "index=0&"
                      "tab=period&"
                      f"period={period}&"
                      # it seems like this variable is changing nothing
                      "homebasededucation=False",
                      verify=False)
        result = {"subject": {}}

        soup = BeautifulSoup(r.text, "lxml")
        try:
            # finds the table and strips out header
            # TODO: rewrite this
            soup = soup.find("table", {"id": "journal"})
            for t in soup.findAll("tr")[2:]:
                subject_name = t.find("strong", {"class": "u"}).text
                marks_list = t.findAll("span", {"class": "mark"})

                result["subject"][subject_name] = {}
                result["subject"][subject_name]["marks"] = []
                # the last 2 marks is average mark and final mark
                for mark in marks_list[:-2]:
                    result["subject"][subject_name]["marks"].append({mark.text: mark["title"]})

                try:
                    result["subject"][subject_name]["mark_average"] = marks_list[-2].text
                except Exception:
                    result["subject"][subject_name]["mark_average"] = None

                result["subject"][subject_name]["mark_final"] = None if not marks_list[-1].text else marks_list[-1].text

            return result
        except Exception as e:
            logger.error(f"During user info parsing this exception accured:\n{e}")

    def get_posts(self, limit: int):
        logger.info("Getting posts")

        self.session.headers["Host"] = "dnevnik.ru"
        self.session.headers["Referer"] = "https://dnevnik.ru/userfeed"

        return json_loads(self._get(f"{self.api_url}userfeed/posts/?limit={limit}").text)
