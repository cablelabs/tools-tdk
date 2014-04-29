package com.comcast.rdk



import grails.test.mixin.*
import org.junit.*

/**
 * See the API for {@link grails.test.mixin.domain.DomainClassUnitTestMixin} for usage instructions
 */
class PrimitiveTestTests {

    @Test
    void testSomething() {
        def t = "s"
        println t.instanceof(String.class)
    }
}

