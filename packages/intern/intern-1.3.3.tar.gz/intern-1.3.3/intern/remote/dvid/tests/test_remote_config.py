# Copyright 2020 The Johns Hopkins University Applied Physics Laboratory
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from intern.remote.dvid import DVIDRemote
from mock import patch, ANY
import unittest


class TestRemoteGetCutout(unittest.TestCase):
    def setUp(self):
        config = {"protocol": "https",
                  "host": "emdata.janelia.org"}

        self.remote = DVIDRemote(config)

if __name__ == '__main__':
    unittest.main()