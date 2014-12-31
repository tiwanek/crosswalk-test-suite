#!/usr/bin/env python

import unittest
import os, sys, commands
import comm

class TestPackertoolsFunctions(unittest.TestCase):
    def test_manifest1(self):
        comm.setUp()
        print os.getcwd()
        os.chdir(comm.ConstPath + "/../testapp/example")
        cmd = "python %smake_apk.py --package=org.xwalk.example --arch=%s --mode=%s --manifest=%s" % \
        (comm.Pck_Tools, comm.ARCH, comm.MODE, comm.MANIFEST_PATH[0])
        packstatus = commands.getstatusoutput(cmd)
        self.assertEquals(0, packstatus[0])
        print "Generate APK ----------------> OK!"
        result = commands.getstatusoutput("ls")
        self.assertIn(comm.AppName, result[1])
        os.remove(comm.AppName)
        os.chdir("../..")

    def test_manifest2(self):
        comm.setUp()
        os.chdir(comm.ConstPath + "/../testapp/example")
        cmd = "python %smake_apk.py --package=org.xwalk.example --arch=%s --mode=%s --manifest=%s" % \
        (comm.Pck_Tools, comm.ARCH, comm.MODE, comm.MANIFEST_PATH[1])
        packstatus = commands.getstatusoutput(cmd)
        self.assertEquals(0, packstatus[0])
        print "Generate APK ----------------> OK!"
        result = commands.getstatusoutput("ls")
        self.assertIn(comm.AppName, result[1])
        os.remove(comm.AppName)
        os.chdir("../..")

    def test_manifest3(self):
        comm.setUp()
        os.chdir(comm.ConstPath + "/../testapp/example")
        cmd = "python %smake_apk.py --package=org.xwalk.example --arch=%s --mode=%s --manifest=%s" % \
        (comm.Pck_Tools, comm.ARCH, comm.MODE, comm.MANIFEST_PATH[2])
        packstatus = commands.getstatusoutput(cmd)
        self.assertEquals(0, packstatus[0])
        print "Generate APK ----------------> OK!"
        result = commands.getstatusoutput("ls")
        self.assertIn(comm.AppName, result[1])
        os.remove(comm.AppName)

    def test_manifest4(self):
        comm.setUp()
        manifestPath = comm.ConstPath + "/../testapp/manifest_no_starturl/manifest.json"
        cmd = "python %smake_apk.py --package=org.xwalk.example --arch=%s --mode=%s --manifest=%s" % \
        (comm.Pck_Tools, comm.ARCH, comm.MODE, manifestPath)
        packstatus = commands.getstatusoutput(cmd)
        errorInfo = "there is no app launch path defined in manifest.json"
        print errorInfo
        self.assertIn(errorInfo, packstatus[1])

if __name__ == '__main__':  
    unittest.main()
