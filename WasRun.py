#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by André Pitombeira on 2012-06-29.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import unittest
import TestCase

class TestCase:
	def __init__(self, name):
		self.name = name
		
	def run(self, result):
		result.testStarted()
		self.setUp()
		try:
			method = getattr(self, self.name)
			method()
		except:
			result.testFailed()
		self.tearDown()
	
	def tearDown():
		pass
	
class TestResult:
	def __init__(self):
		self.runCount = 0
		self.errorCount = 0
		
	def testStarted(self):
		self.runCount = self.runCount + 1	
	
	def testFailed(self):
		self.errorCount = self.errorCount + 1
		
	def summary(self):
		return "%d run, %d failed" % (self.runCount,self.errorCount)
		
class WasRun(TestCase):
	def __init__(self, name):
		TestCase.__init__(self, name)
		
	def setUp(self):
		self.log = "setUp "
		
	def testMethod(self):
		self.log = self.log + "testMethod "
	
	def testBrokenMethod(self):
		raise Exception
	
	def tearDown(self):
		self.log = self.log + "tearDown"

class TestSuite:
	def __init__(self):
		self.tests = []
	
	def add(self, test):
		self.tests.append(test)
	
	def run(self, result):
		for test in self.tests:
			test.run(result)
		
class TestCaseTest(unittest.TestCase):
	def setUp(self):
		self.result = TestResult()	

	def testTemplateMethod(self):
		test = WasRun("testMethod")
		test.run(self.result)
		assert("setUp testMethod tearDown" == test.log)
	
	def testResult(self):
		test = WasRun("testMethod")		
		test.run(self.result)
		assert("1 run, 0 failed" == self.result.summary())
	
	def testFailedResult(self):
		test = WasRun("testBrokenMethod")
		test.run(self.result)
		assert("1 run, 1 failed" == self.result.summary())	
	
	def testFailedResultFormatting(self):
		self.result.testStarted()
		self.result.testFailed()
		assert("1 run, 1 failed" == self.result.summary())
	
	def testSuite(self):
		suite = TestSuite()
		suite.add(WasRun("testMethod"))
		suite.add(WasRun("testBrokenMethod"))
		suite.run(self.result)
		assert("2 run, 1 failed" == self.result.summary())
		
if __name__ == '__main__':
	unittest.main()