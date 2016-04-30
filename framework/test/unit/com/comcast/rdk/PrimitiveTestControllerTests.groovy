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

@TestFor(PrimitiveTestController)
@Mock(PrimitiveTest)
class PrimitiveTestControllerTests {

    def populateValidParams(params) {
        assert params != null
        // TODO: Populate valid properties like...
        //params["name"] = 'someValidName'
    }

    void testIndex() {
        controller.index()
        assert "/primitiveTest/list" == response.redirectedUrl
    }

    void testList() {

        def model = controller.list()

        assert model.primitiveTestInstanceList.size() == 0
        assert model.primitiveTestInstanceTotal == 0
    }

    void testCreate() {
        def model = controller.create()

        assert model.primitiveTestInstance != null
    }

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

    void testShow() {
        controller.show()

        assert flash.message != null
        assert response.redirectedUrl == '/primitiveTest/list'

        populateValidParams(params)
        def primitiveTest = new PrimitiveTest(params)

        assert primitiveTest.save() != null

        params.id = primitiveTest.id

        def model = controller.show()

        assert model.primitiveTestInstance == primitiveTest
    }

    void testEdit() {
        controller.edit()

        assert flash.message != null
        assert response.redirectedUrl == '/primitiveTest/list'

        populateValidParams(params)
        def primitiveTest = new PrimitiveTest(params)

        assert primitiveTest.save() != null

        params.id = primitiveTest.id

        def model = controller.edit()

        assert model.primitiveTestInstance == primitiveTest
    }

    void testUpdate() {
        controller.update()

        assert flash.message != null
        assert response.redirectedUrl == '/primitiveTest/list'

        response.reset()

        populateValidParams(params)
        def primitiveTest = new PrimitiveTest(params)

        assert primitiveTest.save() != null

        // test invalid parameters in update
        params.id = primitiveTest.id
        //TODO: add invalid values to params object

        controller.update()

        assert view == "/primitiveTest/edit"
        assert model.primitiveTestInstance != null

        primitiveTest.clearErrors()

        populateValidParams(params)
        controller.update()

        assert response.redirectedUrl == "/primitiveTest/show/$primitiveTest.id"
        assert flash.message != null

        //test outdated version number
        response.reset()
        primitiveTest.clearErrors()

        populateValidParams(params)
        params.id = primitiveTest.id
        params.version = -1
        controller.update()

        assert view == "/primitiveTest/edit"
        assert model.primitiveTestInstance != null
        assert model.primitiveTestInstance.errors.getFieldError('version')
        assert flash.message != null
    }

    void testDelete() {
        controller.delete()
        assert flash.message != null
        assert response.redirectedUrl == '/primitiveTest/list'

        response.reset()

        populateValidParams(params)
        def primitiveTest = new PrimitiveTest(params)

        assert primitiveTest.save() != null
        assert PrimitiveTest.count() == 1

        params.id = primitiveTest.id

        controller.delete()

        assert PrimitiveTest.count() == 0
        assert PrimitiveTest.get(primitiveTest.id) == null
        assert response.redirectedUrl == '/primitiveTest/list'
    }
}
