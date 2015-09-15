# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock
from oauth2client.client import AccessTokenCredentials
import unittest

# import Python so we can mock the parts we need to here.
import IPython

def noopDecorator(func):
  return func

IPython.core.magic.register_line_cell_magic = noopDecorator
IPython.core.magic.register_line_magic = noopDecorator
IPython.core.magic.register_cell_magic = noopDecorator
IPython.get_ipython = mock.Mock()

import gcp.bigquery
import gcp.datalab

class TestCases(unittest.TestCase):

  @mock.patch('gcp.datalab._bigquery._notebook_environment')
  @mock.patch('gcp.bigquery._create_api')
  def test_udf_cell(self, mock_create_api, mock_notebook_environment):
    env = {}
    cell_body = \
"""
/**
 * @param {{word: string, corpus: string, word_count: integer}} r
 * @param function({{word: string, corpus: string, count: integer}}) emitFn
 */
function(r, emitFn) {
  if (r.word.match(/[shakespeare]/) !== null) {
    var result = { word: r.word, corpus: r.corpus, count: r.word_count };
    emitFn(result);
  }
}
"""
    mock_create_api.return_value = self._create_api()
    mock_notebook_environment.return_value = env
    gcp.datalab._bigquery._udf_cell({'name': 'word_filter'}, cell_body)
    udf = env['word_filter']
    self.assertIsNotNone(udf)
    self.assertEquals('word_filter', udf._name)
    self.assertEquals([('word', 'string'), ('corpus', 'string'), ('word_count', 'integer')],
                      udf._inputs)
    self.assertEquals([('word', 'string'), ('corpus', 'string'), ('count', 'integer')],
                      udf._outputs)
    self.assertEquals(cell_body, udf._implementation)

  def _create_api(self):
    context = self._create_context()
    return gcp.bigquery._api.Api(context.credentials, context.project_id)

  def _create_context(self):
    project_id = 'test'
    creds = AccessTokenCredentials('test_token', 'test_ua')
    return gcp.Context(project_id, creds)

  def test_sample_cell(self):
    # TODO(gram): complete this test
    pass

  def test_udf_cell(self):
    # TODO(gram): complete this test
    pass

  def test_get_schema(self):
    # TODO(gram): complete this test
    pass

  def test_get_table(self):
    # TODO(gram): complete this test
    pass

  def test_table_viewer(self):
    # TODO(gram): complete this test
    pass
