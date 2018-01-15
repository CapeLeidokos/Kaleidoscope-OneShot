#!/usr/bin/python3

# -*- mode: c++ -*-
# Kaleidoscope-Papageno -- Papageno features for Kaleidoscope
# Copyright (C) 2017 noseglasses <shinynoseglasses@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import leidokos
from leidokos import *

from

import sys

class OneShotTest(Test):

   def run(self):
      
      self.description(
"This test checks the import of Python symbols exported by Kaleidoscope-OneShot.\n"
"\n"
      )
      
      aStateT = leidokos.kaleidoscope.one_shot.state_t()
      
      aStateT.mods = 13
      aStateT.layers = 13
      aStateT.all = 1211
      
      one_shot = leidokos.kaleidoscope.one_shot.OneShot()
      
      one_shot.isActive()
      one_shot.isActiveKey(leidokos.Key(145))
      one_shot.isSticky()
      one_shot.cancelWithStickies(True)
      one_shot.cancel()
      one_shot.isModifierActive()
      one_shot.inject(leidokos.Key(145), 111)
      
      self.write("one_shot.time_out = %s" % str(one_shot.time_out))
      self.write("one_shot.hold_time_out = %s" % str(one_shot.hold_time_out))
      self.write("one_shot.double_tap_sticky = %s" % str(one_shot.double_tap_sticky))
      
      self.write("one_shot.start_time_ = %s" % str(one_shot.start_time_))
      self.write("one_shot.state_ = %s" % str(one_shot.state_))
      self.write("one_shot.sticky_state_ = %s" % str(one_shot.sticky_state_))
      self.write("one_shot.pressed_state_ = %s" % str(one_shot.pressed_state_))
      self.write("one_shot.prev_key_ = %s" % str(one_shot.prev_key_))
      self.write("one_shot.should_cancel_ = %s" % str(one_shot.should_cancel_))      self.write("one_shot.should_mask_on_interrupt_ = %s" % str(one_shot.should_mask_on_interrupt_))

def main():
    
   test = OneShotTest()
   test.debug = True
      
   test.run()
   
   #test.graphicalMap()
   
   return test
                   
if __name__ == "__main__":
   global test
   test = main()
