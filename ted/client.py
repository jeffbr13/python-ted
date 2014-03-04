from collections import namedtuple
import logging
import re

from lxml import html
from requests import Session

from .course import Course

class ASPXSession:
    """
    Holds ASPX session variables, which are used for form validation between pages.
    """

    def __init__(self, html):
        """
        Takes HTML page and uses XPath to find session variables.
        """
        try:
            self.viewstate = html.xpath('//input[@name="__VIEWSTATE"]/@value')[0]
            self.eventvalidation = html.xpath('//input[@name="__EVENTVALIDATION"]/@value')[0]
        except:
            raise Exception('Couldn\'t build session - ASPX session fields not found in HTML')

    def parameters(self):
        return {
            '__VIEWSTATE': self.viewstate,
            '__EVENTVALIDATION': self.eventvalidation,
        }


class Client:
    """
    Main interface for interacting with T@Ed.
    """

    default_page = 'https://www.ted.is.ed.ac.uk/UOE1314_SWS/default.aspx'

    def __init__(self):
        """
        Initialise T@Ed session and download course list.
        """
        self.session = Session()

        # Get ASPX session variables from default page:
        response = self.session.get('https://www.ted.is.ed.ac.uk/UOE1314_SWS/default.aspx', verify=False)
        index = html.document_fromstring(response.text)
        self.aspx_session = ASPXSession(index)

        # Get course-list page:
        parameters = {
            '__EVENTTARGET': 'LinkBtn_modules',
            'tLinkType': 'information',
        }
        course_page = self.post(Client.default_page, parameters=parameters)
        course_options = course_page.xpath('//select[@name="dlObject"]/option')

        # Process courses:
        self.courses = []
        for option in course_options:
            try:
                title, identifier = option.text.strip().rsplit(' - ', 1)
            except ValueError as e:
                logging.warning('Error in splitting {0}, title and identifier will be the same: {1}'.format(option.text.strip(), e))
                title = identifier = option.text.strip()
            code = identifier[:9]
            self.courses.append(Course(title=title,
                                       identifier=identifier,
                                       code=code))
        return


    def get(self, url, parameters):
        """
        Get a webpage, returning HTML.
        """
        parameters.update(self.aspx_session.parameters())
        response = self.session.get(url, params=parameters, verify=False)
        page = html.document_fromstring(response.text)
        self.aspx_session = ASPXSession(page)
        return page

    def post(self, url, parameters):
        """
        Post data to a webpage, returning HTML.
        """
        parameters.update(self.aspx_session.parameters())
        response = self.session.post(url, data=parameters, verify=False)
        page = html.document_fromstring(response.text)
        self.aspx_session = ASPXSession(page)
        return page


    def search(self, regex):
        """
        Returns a list of all courses which have an attribute matching the given regex.
        """
        return [c for c in self.courses if regex.match(c.title)
                                        or regex.match(c.code)
                                        or regex.match(c.identifier)]


    def course(self, course_code=None):
        for c in self.courses:
            if course_code in c.code:
                return c

