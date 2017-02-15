"""Test video searching."""

import unittest, os
from youtube.selector_helper import Selector
from youtube.search import YouTubeSearch

"""
Page 1 video: https://www.youtube.com/watch?v=WlRxNSRA7Rg
Page 3 video: https://www.youtube.com/watch?v=tDkmhZIQ9jo
Non-existent video: https://www.youtube.com/watch?v=PH34kMOjmQk
"""


class VideoSearchTestCase(unittest.TestCase):
    SEARCH_PAGE_URL = 'file://' + os.path.abspath('./tests/resources/'
                                                  'search_1.html')

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _mocked_query_youtube(self):
        return self._ys_driver

    def _mock_query_youtube(self, ys):
        """Mocks the YouTubeSearch.query_youtube() method"""
        ys.driver.get(self.SEARCH_PAGE_URL)
        self._ys_driver = ys.driver
        ys.query_youtube = self._mocked_query_youtube


    def test_video_found_on_first_page(self):
        video_id = 'WlRxNSRA7Rg'
        search_terms = ['cute cats']  # not used in this test
        max_page = 4

        ys = YouTubeSearch(video_id=video_id, search_terms=search_terms,
                           max_page=max_page)
        self._mock_query_youtube(ys)
        video_search_info = ys.search()
        self.assertIsNotNone(video_search_info)

        driver = ys.driver
        expected_elem = driver.find_element_by_xpath(
                Selector.get_xpath_video_selector(video_id=video_id))
        # video_search_info is what will be passed to the YouTubePlayer
        # module. Besides other things, it contains the element which will
        # be clicked() on by the YouTubePlayer to play the video.
        self.assertEqual(video_search_info['page'], 1)
        self.assertEqual(video_search_info['search_term'], 'cute cats')
        self.assertEqual(video_search_info['video_element'], expected_elem)

        ys.close_driver()

    def test_video_found_on_third_page(self):
        video_id = 'tDkmhZIQ9jo'
        search_terms = ['cute cats']  # not used in this test
        max_page = 4

        ys = YouTubeSearch(video_id=video_id, search_terms=search_terms,
                           max_page=max_page)
        self._mock_query_youtube(ys)
        video_search_info = ys.search()
        self.assertIsNotNone(video_search_info)

        driver = ys.driver
        expected_elem = driver.find_element_by_xpath(
                Selector.get_xpath_video_selector(video_id=video_id))
        # video_search_info is what will be passed to the YouTubePlayer
        # module. Besides other things, it contains the element which will
        # be clicked() on by the YouTubePlayer to play the video.
        self.assertEqual(video_search_info['page'], 3)
        self.assertEqual(video_search_info['search_term'], 'cute cats')
        self.assertEqual(video_search_info['video_element'], expected_elem)
        ys.close_driver()

    def test_video_not_found(self):
        video_id = 'PH34kMOjmQk'
        search_terms = ['cute cats']  # not used in this test
        max_page = 4

        ys = YouTubeSearch(video_id=video_id, search_terms=search_terms,
                           max_page=max_page)
        self._mock_query_youtube(ys)
        video_search_info = ys.search()
        # if the video is not found, None is returned
        self.assertIsNone(video_search_info)
        ys.close_driver()
