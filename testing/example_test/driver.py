#!/usr/bin/python3

# Import control stuff like assertions, test, etc.
#
from leidokos import *

# Import exported symbols from C++
#
import kaleidoscope
from kaleidoscope.one_shot import OneShot
            
class OneShotTestDriver(TestDriver):
   
   def dumpIndented(self, msg):
      self.out.write("   " + msg )
      
   def dumpOneShot(self):
            
      self.out.write("OneShot state\n")
      self.dumpIndented("OneShot.time_out = %s\n" % OneShot.time_out)
      self.dumpIndented("OneShot.hold_time_out = %s\n" % OneShot.hold_time_out)
      self.dumpIndented("OneShot.double_tap_sticky = %s\n" % OneShot.double_tap_sticky)
      
      self.dumpIndented("OneShot.start_time_ = %s\n" % OneShot.start_time_)
      self.dumpIndented("OneShot.state_.mods = %s\n" % OneShot.state_.mods)
      self.dumpIndented("OneShot.state_.layers = %s\n" % OneShot.state_.layers)
      self.dumpIndented("OneShot.sticky_state_.mods = %s\n" % OneShot.sticky_state_.mods)
      self.dumpIndented("OneShot.sticky_state_.layers = %s\n" % OneShot.sticky_state_.layers)
      self.dumpIndented("OneShot.sticky_state_.all = %s\n" % OneShot.sticky_state_.all)
      self.dumpIndented("OneShot.pressed_state_.mods = %s\n" % OneShot.pressed_state_.mods)
      self.dumpIndented("OneShot.pressed_state_.layers = %s\n" % OneShot.pressed_state_.layers)
      self.dumpIndented("OneShot.pressed_state_.all = %s\n" % OneShot.pressed_state_.all)
      self.dumpIndented("OneShot.prev_key_.keyCode = %s\n" % OneShot.prev_key_.keyCode)
      self.dumpIndented("OneShot.prev_key_.flags = %s\n" % OneShot.prev_key_.flags)
      self.dumpIndented("OneShot.should_cancel_ = %s\n" % OneShot.should_cancel_)
      self.dumpIndented("OneShot.should_mask_on_interrupt_ = %s\n" % OneShot.should_mask_on_interrupt_)
      self.out.write("\n")
      
   def run(self):
      
      # Automatically have all reports dumped. This helps during
      # test setup and debugging when we do not exactly know when
      # to expect a report and what it contains.
      #
      self.addPermanentReportAssertions([DumpReport()])
      
      # Define some keymap positions
      #
      self.keymap_A_keypos = (2, 1)
      self.keymap_OSL_Left_Shift_keypos = (3, 7)
      
      # The number of cycles we allow to elapse when we call scanCycles(...)
      #
      self.scanCyclesDefaultCount = 5
      
      # Dump overall settings
      #
      self.header("Settings")
      self.log("OSL(LeftShift) at %s" % str(self.keymap_OSL_Left_Shift_keypos))
      self.log("Key_A at %s" % str(self.keymap_A_keypos))
      self.log("interval cycles: %s" % str(self.scanCyclesDefaultCount))
      self.out.write("\n")
      
      # Run tests
      # Important: Allways use runTest(...) as this automatically
      #            initializes the keyboard and the testing system before
      #            each test.
      #
      self.runTest("checkOSL")
      self.runTest("checkOSLTimeout")
      
   def checkOSL(self):
      
      self.description(
         "\n"
         "This test checks one shot modifiers of Kaleidoscope-OneShot.\n"
         "\n"
      )
      
      # Perform some initial scan cycles to catch potential timing errors
      #
      self.header("Initialization")
      self.scanCycles(onStopAssertionList = [NReportsGenerated(0)])
      
      # Dump the OneShot initial state
      #
      self.header("Initial state")
      self.dumpOneShot()
      
      # Press the one shot shift key. 
      # This must activate the left shift by sending exactly one key report.
      #
      self.header("Pressing OSM(LeftShift)")
      self.keyDown(*self.keymap_OSL_Left_Shift_keypos)
      self.queueGroupedReportAssertions([ 
         ReportAllKeysInactive(),
         ReportModifiersActive([keyLShift()], exclusively = True)
      ])
      self.scanCycles(onStopAssertionList = [NReportsGenerated(1)])
      self.dumpOneShot()
      
      # Release the one shot shift key.
      # This must not cause any key reports.
      #
      self.header("Releasing OSM(LeftShift)")
      self.keyUp(*self.keymap_OSL_Left_Shift_keypos)
      self.scanCycles(onStopAssertionList = [NReportsGenerated(0)])
      self.dumpOneShot()
      
      # Press a letter key (a) that is expected to be turned
      # uppercase. This is expected to cause a keyreport that
      # contains the key and the shift modifier.
      # In the next cycle, the shift modifier is released (one shot).
      #
      self.header("Pressing Key_A")
      self.keyDown(*self.keymap_A_keypos)
      # Expect the shifted A key in the report
      self.queueGroupedReportAssertions([ 
         ReportKeysActive([keyA()], exclusively = True),
         ReportModifiersActive([keyLShift()], exclusively = True)
      ])
      self.scanCycle([CycleHasNReports(1)])
      self.dumpOneShot()
      self.queueGroupedReportAssertions([ 
         ReportKeysActive([keyA()], exclusively = True),
         ReportAllModifiersInactive()
      ])
      self.scanCycle([CycleHasNReports(1)])
      self.dumpOneShot()
      
      # Release the key. An empty report is expected.
      #
      self.header("Releasing Key_A")
      self.keyUp(*self.keymap_A_keypos)
      # Expect an empty report
      self.queueGroupedReportAssertions([ 
         ReportEmpty()
      ])
      self.scanCycles(onStopAssertionList = [NReportsGenerated(1)])
      self.dumpOneShot()

   def checkOSLTimeout(self):
      
      self.description(
"\n"
"This test checks timeout of one shot modifiers of Kaleidoscope-OneShot.\n"
"\n"
      )
      
      self.header("Initialization")
      self.scanCycles(onStopAssertionList = [NReportsGenerated(0)])
      
      self.header("Initial state")
      self.dumpOneShot()
      
      self.header("Pressing OSM(LeftShift)")
      self.keyDown(*self.keymap_OSL_Left_Shift_keypos)
      self.queueGroupedReportAssertions([ 
         ReportAllKeysInactive(),
         ReportModifiersActive([keyLShift()], exclusively = True)
      ])
      self.scanCycles(onStopAssertionList = [NReportsGenerated(1)])
      self.dumpOneShot()
      
      self.header("Releasing OSM(LeftShift)")
      self.keyUp(*self.keymap_OSL_Left_Shift_keypos)
      self.scanCycle([CycleHasNReports(0)])
      self.dumpOneShot()
      
      # Waiting for a time that is longer than OneShot's timeout
      # ensures that the one shot modifier is cleared.
      #
      self.header("Have a break longer than the timeout")
      self.queueGroupedReportAssertions([ 
         ReportEmpty()
      ])
      self.skipTime(2*OneShot.time_out,
                    [NReportsGenerated(1)])
      
      # Assert that the key is reported without shift modifier.
      #
      self.header("Pressing Key_A")
      self.keyDown(*self.keymap_A_keypos)
      # Expect the shifted A key in the report
      self.queueGroupedReportAssertions([ 
         ReportKeysActive([keyA()], exclusively = True),
         ReportAllModifiersInactive()
      ])
      self.scanCycles(onStopAssertionList = [NReportsGenerated(1)])
      self.dumpOneShot()
      
      self.header("Releasing Key_A")
      self.keyUp(*self.keymap_A_keypos)
      # Expect an empty report
      self.queueGroupedReportAssertions([ 
         ReportEmpty()
      ])
      self.scanCycles(onStopAssertionList = [NReportsGenerated(1)])
      self.dumpOneShot()

def main():
    
   driver = OneShotTestDriver()
   driver.debug = True
      
   driver.run()
   
   return driver
                   
if __name__ == "__main__":
   global driver
   driver = main()
