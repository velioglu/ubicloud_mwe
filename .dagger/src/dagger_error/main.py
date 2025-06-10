from dagger import dag, function, object_type, Container, Directory

@object_type
class DaggerError:

    @function
    async def kotlin_test_build(self, source: Directory) -> Container:
        """Prepares the test build container"""
        return (
            dag.container()
            .from_("gradle:8.11.1-jdk21-alpine")
            .with_mounted_directory("/app", source)
            .with_workdir("/app")
            # .with_exec(["gradle", "buildFatJar", "--no-daemon"])
        )

    @function
    async def build_and_test(self, source: Directory) -> str:
        """Builds the Kotlin application and runs tests, returning test results"""
        test_build = await self.kotlin_test_build(source)
        return await (
            test_build
            .with_service_binding("docker", dag.testcontainers().docker_service())
            .with_env_variable("DOCKER_HOST", "tcp://docker:2375")
            .with_env_variable("TESTCONTAINERS_RYUK_DISABLED", "true")
            .with_exec(["gradle", "kotest"])
            .stderr()
        )

    @function
    async def test_without_docker(self, source: Directory) -> str:
        """Alternative: Runs tests with Docker disabled for Testcontainers"""
        test_build = await self.kotlin_test_build(source)
        return await (
            test_build
            .with_env_variable("TESTCONTAINERS_CHECKS_DISABLE", "true")
            .with_exec(["gradle", "kotest"])
            .stderr()
        )
