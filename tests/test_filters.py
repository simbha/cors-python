import unittest
import errors
import filters
from cors_options import CorsOptions
from cors_handler import CorsRequest
from cors_handler import CorsResponse


class TestAllowCredentialsFilter(unittest.TestCase):

    def test_addHeader(self):
        options = CorsOptions(allow_credentials=True)
        response = CorsResponse()
        f = filters.AllowCredentialsFilter(options)
        f.filter(None, response)
        self.assertTrue(response.allow_credentials)

    def test_noHeader(self):
        options = CorsOptions(allow_credentials=False)
        response = CorsResponse()
        f = filters.AllowCredentialsFilter(options)
        f.filter(None, response)
        self.assertFalse(response.allow_credentials)


class TestAllowNonCorsRequestFilter(unittest.TestCase):

    def test_allow(self):
        options = CorsOptions(allow_non_cors_requests=True)
        f = filters.AllowNonCorsRequestFilter(options)
        error = f.filter(None, None)
        self.assertIsNone(error)

    def test_disallow(self):
        options = CorsOptions(allow_non_cors_requests=False)
        f = filters.AllowNonCorsRequestFilter(options)
        error = f.filter(None, None)
        self.assertIsNotNone(error)


class TestAllowOriginFilter(unittest.TestCase):

    def test_allowAllOrigins(self):
        options = CorsOptions()
        f = filters.AllowOriginFilter(options)

        # Test with no Origin
        request = CorsRequest()
        response = CorsResponse()
        error = f.filter(request, response)
        self.assertIsNone(error)
        self.assertEquals('*', response.allow_origin)

        # Test CORS request
        request = CorsRequest('GET', {'Origin': 'http://foo.com'})
        response = CorsResponse()
        error = f.filter(request, response)
        self.assertIsNone(error)
        self.assertEquals('*', response.allow_origin)

        # Test CORS preflight request
        request = CorsRequest('OPTIONS', {
          'Origin': 'http://foo.com',
          'Access-Control-Request-Method': 'GET'
        })
        response = CorsResponse()
        error = f.filter(request, response)
        self.assertIsNone(error)
        self.assertEquals('*', response.allow_origin)

    def test_invalidOrigin(self):
        options = CorsOptions(allow_origins=['http://foo.com'])
        f = filters.AllowOriginFilter(options)
        request = CorsRequest('GET', {'Origin': 'http://bar.com'})
        response = CorsResponse()
        error = f.filter(request, response)
        self.assertIsInstance(error, errors.OriginError)
        self.assertIsNone(response.allow_origin)

    def test_validOrigin(self):
        options = CorsOptions(allow_origins=['http://foo.com'])
        f = filters.AllowOriginFilter(options)
        request = CorsRequest('GET', {'Origin': 'http://foo.com'})
        response = CorsResponse()
        error = f.filter(request, response)
        self.assertIsNone(error)
        self.assertEquals('http://foo.com', response.allow_origin)

    def test_allowCredentials(self):
        options = CorsOptions(allow_origins=True,
                              allow_credentials=True)
        f = filters.AllowOriginFilter(options)
        request = CorsRequest('GET', {'Origin': 'http://foo.com'})
        response = CorsResponse()
        error = f.filter(request, response)
        self.assertIsNone(error)
        self.assertEquals('http://foo.com', response.allow_origin)


class TestExposeHeadersFilter(unittest.TestCase):

    def test_noHeader(self):
        options = CorsOptions()
        response = CorsResponse()
        f = filters.ExposeHeadersFilter(options)
        f.filter(None, response)
        self.assertEquals(0, len(response.expose_headers))

    def test_addHeader(self):
        options = CorsOptions(expose_headers=["Foo"])
        response = CorsResponse()
        f = filters.ExposeHeadersFilter(options)
        f.filter(None, response)
        self.assertEquals(1, len(response.expose_headers))
        self.assertEquals('Foo', response.expose_headers[0])


class TestMaxAgeFilter(unittest.TestCase):

    def test_noHeader(self):
        options = CorsOptions()
        response = CorsResponse()
        f = filters.MaxAgeFilter(options)
        f.filter(None, response)
        self.assertIsNone(response.max_age)

    def test_addHeader(self):
        options = CorsOptions(max_age=1000)
        response = CorsResponse()
        f = filters.MaxAgeFilter(options)
        f.filter(None, response)
        self.assertEquals(1000, response.max_age)


class TestVaryFilter(unittest.TestCase):

    def test_addHeader(self):
        options = CorsOptions(vary=True)
        response = CorsResponse()
        filtr = filters.VaryFilter(options)
        filtr.filter(None, response)
        self.assertEquals('Origin', response.headers['Vary'])

    def test_noHeader(self):
        options = CorsOptions(vary=False)
        response = CorsResponse()
        filtr = filters.VaryFilter(options)
        filtr.filter(None, response)
        self.assertFalse('Vary' in response.headers)


if __name__ == '__main__':
    unittest.main()
