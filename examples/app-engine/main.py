#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from cors.cors_application import CorsApplication
from cors.cors_options import CorsOptions


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

webapp = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
app = CorsApplication(webapp, CorsOptions(allow_origins=['http://blah.com'],
                                          allow_headers=['X-Foo'],
                                          continue_on_error=True))