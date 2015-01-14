#!/usr/bin/env python
#
# Copyright (c) 2015 Intel Corporation.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of works must retain the original copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the original copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of Intel Corporation nor the names of its contributors
#   may be used to endorse or promote products derived from this work without
#   specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY INTEL CORPORATION "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL INTEL CORPORATION BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors:
#         Hongjuan, Wang<hongjuanx.wang@intel.com>

import unittest
import os, sys, commands, shutil, stat
import comm

class TestPackertoolsFunctions(unittest.TestCase):
    def test_projectdir_readOnly(self):
        comm.setUp()
        os.chdir(comm.Pck_Tools)
        manifestPath = comm.ConstPath + "/../testapp/example/manifest.json"
        if not os.path.exists(comm.Pck_Tools + "readOnly"):
            os.mkdir("readOnly")
        os.chmod("readOnly", stat.S_IREAD)
        cmd = "python make_apk.py --package=org.xwalk.example --arch=%s --mode=%s --manifest=%s --project-dir=readOnly" % \
              (comm.ARCH, comm.MODE, manifestPath)
        packstatus = commands.getstatusoutput(cmd)
        errormsg = "OSError: [Errno 13] Permission denied"
        self.assertNotEqual(packstatus[0] ,0)
        self.assertIn(errormsg, packstatus[1])
        self.assertIn(comm.AppName, os.listdir(comm.Pck_Tools))
        try:
            shutil.rmtree(comm.Pck_Tools + "readOnly")
            os.remove(comm.Pck_Tools + comm.AppName)
        except Exception,e:
            os.system("rm -rf "  + comm.Pck_Tools + "readOnly &>/dev/null")
            os.system("rm -rf "  + comm.Pck_Tools + "*apk &>/dev/null")

    def test_projectdir_existFile(self):
        comm.setUp()
        os.chdir(comm.Pck_Tools)
        manifestPath = comm.ConstPath + "/../testapp/example/manifest.json"
        if "existFile.txt" not in os.listdir(comm.Pck_Tools):
            os.mknod("existFile.txt")
        cmd = "python make_apk.py --package=org.xwalk.example --arch=%s --mode=%s --manifest=%s --project-dir=existFile.txt" % \
              (comm.ARCH, comm.MODE, manifestPath)
        packstatus = commands.getstatusoutput(cmd)
        errormsg = "Unable to create a project directory during the build"
        self.assertEqual(packstatus[0] ,0)
        self.assertIn(errormsg, packstatus[1])
        self.assertIn(comm.AppName, os.listdir(comm.Pck_Tools))
        os.remove(comm.Pck_Tools + "/existFile.txt")
        os.remove(comm.Pck_Tools + comm.AppName)

    def test_projectdir_existDir(self):
        comm.setUp()
        os.chdir(comm.Pck_Tools)
        manifestPath = comm.ConstPath + "/../testapp/example/manifest.json"
        if not os.path.exists(comm.Pck_Tools + "testapp"):
            os.makedirs("testapp/testapp")
        cmd = "python make_apk.py --package=org.xwalk.example --arch=%s --mode=%s --manifest=%s --project-dir=testapp/testapp" % \
              (comm.ARCH, comm.MODE, manifestPath)
        packstatus = commands.getstatusoutput(cmd)
        self.assertEqual(packstatus[0] ,0)
        buildDir = comm.Pck_Tools + "testapp/testapp/Example"
        buildList = os.listdir(buildDir)
        self.assertTrue(os.path.isdir(buildDir + "/res"))
        self.assertIn("res", buildList)
        self.assertTrue(os.path.isfile(buildDir + "/build.xml"))
        self.assertIn("build.xml", buildList)
        try:
            shutil.rmtree(comm.Pck_Tools + "testapp")
            os.remove(comm.Pck_Tools + comm.AppName)
        except Exception,e:
            os.system("rm -rf "  + comm.Pck_Tools + "testapp &>/dev/null")
            os.system("rm -rf "  + comm.Pck_Tools + "*apk &>/dev/null")


    def test_projectdir_antbuild(self):
        comm.setUp()
        if os.path.exists(comm.Pck_Tools + "example"):
            try:
                shutil.rmtree(comm.Pck_Tools + "example")
                os.remove(comm.Pck_Tools + comm.AppName)
            except Exception,e:
                os.system("rm -rf "  + comm.Pck_Tools + "example &>/dev/null")
                os.system("rm -rf "  + comm.Pck_Tools + "*apk &>/dev/null")
        os.chdir(comm.Pck_Tools)
        manifestPath = comm.ConstPath + "/../testapp/example/manifest.json"
        cmd = "python make_apk.py --package=org.xwalk.example --arch=%s --mode=%s --manifest=%s --project-dir=example" % \
              (comm.ARCH, comm.MODE, manifestPath)
        packstatus = commands.getstatusoutput(cmd)
        self.assertEqual(packstatus[0] ,0)
        os.remove(comm.Pck_Tools + comm.AppName)
        buildDir = comm.Pck_Tools + "example/Example"
        buildList = os.listdir(buildDir)
        self.assertIn("res", buildList)
        self.assertIn("bin", buildList)
        self.assertIn("AndroidManifest.xml", buildList)
        buildstatus = commands.getstatusoutput("ant release -f " + buildDir + "/build.xml")
        self.assertEqual(buildstatus[0] ,0)
        apkName = "Example-release.apk"
        self.assertIn(apkName, os.listdir(buildDir + "/bin"))
        shutil.copyfile(buildDir + "/bin/" + apkName, comm.Pck_Tools + comm.AppName)
        inststatus = commands.getstatusoutput("adb -s " + comm.device + " install -r " + comm.AppName)
        self.assertEquals(0, inststatus[0])
        print "Install APK ----------------> OK"
        pmstatus = commands.getstatusoutput("adb -s " + comm.device + " shell pm list packages |grep org.xwalk.example")
        self.assertEquals(0, pmstatus[0])
        print "Find Package in comm.device ---------------->O.K"
        launchstatus = commands.getstatusoutput("adb -s " + comm.device + " shell am start -n org.xwalk.example/.ExampleActivity")
        self.assertEquals(0, launchstatus[0])
        print "Launch APK ---------------->OK"
        stopstatus = commands.getstatusoutput("adb -s " + comm.device + " shell am force-stop org.xwalk.example")
        if stopstatus[0] == 0:
            print "Stop APK ---------------->O.K"
            unistatus = commands.getstatusoutput("adb -s " + comm.device + " uninstall org.xwalk.example")
            self.assertEquals(0, unistatus[0])
            print "Uninstall APK ---------------->O.K"
        else:
            print "Stop APK ---------------->Error"
            os.system("adb -s " + comm.device + " uninstall org.xwalk.example")
        if os.path.exists(comm.Pck_Tools + "example"):
            try:
                shutil.rmtree(comm.Pck_Tools + "example")
                os.remove(comm.Pck_Tools + comm.AppName)
            except Exception,e:
                os.system("rm -rf "  + comm.Pck_Tools + "example &>/dev/null")
                os.system("rm -rf "  + comm.Pck_Tools + "*apk &>/dev/null")

if __name__ == '__main__':
    unittest.main()