from collections import namedtuple
import re

from lxml import html
from requests import Session



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

    def __init__(self):
        """
        Initialise T@Ed session and download course list.
        """
        self.session = Session()

        response = self.session.get('https://www.ted.is.ed.ac.uk/UOE1314_SWS/default.aspx', verify=False)
        index = html.document_fromstring(response)
        self.aspx_session = ASPXSession(index)

        parameters = {
            '__EVENTTARGET': 'LinkBtn_modules',
            'tLinkType': 'information',
        }
        parameters.update(self.aspx_session.parameters())

        response = self.session.post('https://www.ted.is.ed.ac.uk/UOE1314_SWS/default.aspx', data=parameters, verify=False)
        course_page = html.document_fromstring(response)
        course_options = course_page.xpath('//select[@name=dlObject]/option')

        self.courses = []
        for option in course_options:
            title, identifier = option.text.strip().rsplit(' - ', 1)
            code = identifier[:9]
            self.courses.append(Course(title=title,
                                       identifier=identifier,
                                       code=code))
        return


    def search(self, regex):
        """
        Returns a list of all courses which have an attribute matching the given regex.
        """
        return [c for c in self.courses if regex.match(c.title)
                                        or regex.match(c.code)
                                        or regex.match(c.identifier)]


    def course(self, course_code=None):
        for c in self.courses:
            if course_code_str in c.code:
                return c

