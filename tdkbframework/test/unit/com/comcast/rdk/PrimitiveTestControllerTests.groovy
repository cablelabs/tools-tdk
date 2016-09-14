/*
 * ============================================================================
 * COMCAST CONFIDENTIAL AND PROPRIETARY
 * ============================================================================
 * This file and its contents are the intellectual property of Comcast.  It may
 * not be used, copied, distributed or otherwise  disclosed in whole or in part
 * without the express written permission of Comcast.
 * ============================================================================
 * Copyright (c) 2016 Comcast. All rights reserved.
 * ============================================================================
 */
package com.comcast.rdk

import org.junit.*
import grails.test.mixin.*

/**
 * Test class for primitive test controller.
 *
 */
@TestFor(PrimitiveTestController)
@Mock(PrimitiveTest)
class PrimitiveTestControllerTests {

	/**
	 * To populate valid params
	 * @param params
	 * @return
	 */
	def populateValidParams(params) {
		assert params != null
	}


	/**
	 * to test the save method
	 */
	void testSave() {
		controller.save()

		assert model.primitiveTestInstance != null
		assert view == '/primitiveTest/create'

		response.reset()

		populateValidParams(params)
		controller.save()

		assert response.redirectedUrl == '/primitiveTest/show/1'
		assert controller.flash.message != null
		assert PrimitiveTest.count() == 1
	}


	/**
	 * to test the index.
	 */
	void testIndex() {
		controller.index()
		assert "/primitiveTest/list" == response.redirectedUrl
	}


	/**
	 * to test the list method
	 */
	void testList() {

		def modelObj = controller.list()

		assert modelObj.primitiveTestInstanceList.size() == 0
		assert modelObj.primitiveTestInstanceTotal == 0
	}



	/**
	 * to test the show method
	 */
	void testShow() {
		controller.show()

		assert flash.message != null
		assert response.redirectedUrl == '/primitiveTest/list'
		//check the params
		populateValidParams(params)
		def primitiveTestObj = new PrimitiveTest(params)
		//check the save
		assert primitiveTestObj.save() != null

		params.id = primitiveTestObj.id
		//invoking show
		def model = controller.show()

		assert model.primitiveTestInstance == primitiveTestObj
	}


	/**
	 * to test the delete method
	 */
	void testDelete() {
		controller.delete()
		assert flash.message != null
		assert response.redirectedUrl == '/primitiveTest/list'

		response.reset()
		//check the params
		populateValidParams(params)
		def primitiveTestObj = new PrimitiveTest(params)
		//check the save
		assert primitiveTestObj.save() != null
		assert PrimitiveTest.count() == 1

		params.id = primitiveTestObj.id
		//invoking delete
		controller.delete()

		assert PrimitiveTest.count() == 0
		assert PrimitiveTest.get(primitiveTestObj.id) == null
		assert response.redirectedUrl == '/primitiveTest/list'
	}

	/**
	 * to test the create method
	 */
	void testCreate() {
		def modelObj = controller.create()
		//check the create return
		assert modelObj.primitiveTestInstance != null
	}

	/**
	 * to test the update method
	 */
	void testUpdate() {
		controller.update()

		assert flash.message != null
		assert response.redirectedUrl == '/primitiveTest/list'

		response.reset()
		//check the params
		populateValidParams(params)
		def primitiveTestObj = new PrimitiveTest(params)
		//check the save
		assert primitiveTestObj.save() != null

		params.id = primitiveTestObj.id

		controller.update()

		assert view == "/primitiveTest/edit"
		assert model.primitiveTestInstance != null

		primitiveTestObj.clearErrors()
		//check the params
		populateValidParams(params)
		controller.update()

		assert response.redirectedUrl == "/primitiveTest/show/$primitiveTestObj.id"
		assert flash.message != null

		//test outdated version number
		response.reset()
		primitiveTestObj.clearErrors()
		//check the params
		populateValidParams(params)
		params.id = primitiveTestObj.id
		params.version = -1
		controller.update()

		assert view == "/primitiveTest/edit"
		assert model.primitiveTestInstance != null
		assert model.primitiveTestInstance.errors.getFieldError('version')
		assert flash.message != null
	}

	/**
	 * to test the edit method
	 */
	void testEdit() {

		controller.edit()

		assert flash.message != null
		assert response.redirectedUrl == '/primitiveTest/list'
		//check the params
		populateValidParams(params)
		def primitiveTest = new PrimitiveTest(params)
		// to test the save return
		assert primitiveTest.save() != null

		params.id = primitiveTest.id
		def model = controller.edit()

		assert model.primitiveTestInstance == primitiveTest
	}
}
