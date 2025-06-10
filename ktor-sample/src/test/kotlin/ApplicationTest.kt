package com.example

import io.kotest.core.spec.style.FunSpec
import io.kotest.matchers.shouldBe
import io.kotest.mpp.log
import org.testcontainers.containers.GenericContainer

class ApplicationTest : FunSpec({
/**
     * Test case verifying that an Alpine Linux container can execute a simple command and output "Hello World".
     *
     * This test demonstrates:
     * - Creating a Docker container using Testcontainers
     * - Starting the container
     * - Executing a shell command inside the container
     * - Verifying the command's output
     */

    test("Alpine container should say Hello World") {
        val alpine = GenericContainer("alpine:3.19")
            .withCommand("sh", "-c", "echo Hello World")
        try {
            alpine.start()
        } catch (e: Exception) {
            println("Failed to start container: ${e.message}")
            throw e
        }
        alpine.logs shouldBe "Hello World\n"
    }
})