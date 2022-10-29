## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          trig_tm_prediction.py
#
#      PURPOSE:
#          Implementation of context menu
#
#------------------------------------------------------------------
import os
import KcsDiminutionList
import KcsGaugedList
import KcsPredictList
import KcsTMList
import kcs_util
import kcs_tm

def pre(*args):                            # pre trigger definition

   #
   # [in]  args[0] - gaugedValuesMode; 1=Min, 2=Average, 3=Max
   # [in]  args[1] - KcsModel
   # [in]  args[2] - KcsTMList
   # [out] args[3] - KcsPredictListMin
   # [out] args[4] - KcsPredictListAverage
   # [out] args[5] - KcsPredictListMax
   #

   # Executes external program as a sub-process
   #
   #exeIn, exeOut = os.popen2('c:\\prediction\\bin\\Pytest.exe')
   exeIn, exeOut = os.popen2('c:\\viewstore\\tmpyt\\Pytest.exe')

   models = args[1]
   for model in models:
      noData = args[2].getNoOfData()
      for x in range( 0, noData):
         tmList = args[2].getListOfDiminution(x)

         # Retrieve and add Thickness Messaurement data
         #
         if args[0] == 1:
            kcs_tm.getTMListMin(model,tmList)
         elif args[0] == 2:
            kcs_tm.getTMListAverage(model,tmList)
         elif args[0] == 3:
            kcs_tm.getTMListMax(model,tmList)
         else:
            print ("Error - undefined mode.")


         noGauged = tmList.GetNumberListOfGauged()
         for y in range( 0, noGauged ):
            gaVal =  tmList.getListOfGauged(y)
            lastDim = gaVal.getDiminution1()

         if noGauged == 0:
            lastDim = 0.5

         # Add data to result list - Min
         #
         listPmin = KcsPredictList.PredictionList()
         listPmin.setDiminutionCalcYear(tmList.getDiminutionCalcYear())
         listPmin.setDiminutionCalcMonth(tmList.getDiminutionCalcMonth())
         listPmin.setDiminutionCalcDay(tmList.getDiminutionCalcDay())
         listPmin.setOriginalThickness1(tmList.getOriginalThickness1())
         args[3].append(listPmin)


         # Add data to result list - Average
         #
         listPaverage = KcsPredictList.PredictionList()
         listPaverage.setDiminutionCalcYear(tmList.getDiminutionCalcYear())
         listPaverage.setDiminutionCalcMonth(tmList.getDiminutionCalcMonth())
         listPaverage.setDiminutionCalcDay(tmList.getDiminutionCalcDay())
         listPaverage.setOriginalThickness1(tmList.getOriginalThickness1())
         args[4].append(listPaverage)


         # Add data to result list - Max
         #
         listPmax = KcsPredictList.PredictionList()
         listPmax.setDiminutionCalcYear(tmList.getDiminutionCalcYear())
         listPmax.setDiminutionCalcMonth(tmList.getDiminutionCalcMonth())
         listPmax.setDiminutionCalcDay(tmList.getDiminutionCalcDay())
         listPmax.setOriginalThickness1(tmList.getOriginalThickness1())
         args[5].append(listPmax)


         # Send data to external program
         #
         exeIn.write(str(lastDim)  + '\n')

   # Terminate external program input sequence
   #
   exeIn.write('-999\n')	

   # Retrieve data from external program and add to result list - Average
   #
   m = 0
   for model in models:
      noData = args[2].getNoOfData()
      for x in range( 0, noData ):
         outData = exeOut.readline()
         outData  = outData [:-1]
         args[3][x+(noData*m)].setPredictedDiminution(float(outData))
         outData = exeOut.readline()
         outData  = outData [:-1]
         args[4][x+(noData*m)].setPredictedDiminution(float(outData))
         outData = exeOut.readline()
         outData  = outData [:-1]
         args[5][x+(noData*m)].setPredictedDiminution(float(outData))
      m = m + 1
   args[2].setNoOfData(0)
   result = kcs_util.trigger_ok()
   return result
