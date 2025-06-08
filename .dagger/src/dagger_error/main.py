from dagger import dag, function, object_type, Container, Directory

@object_type
class DaggerError:
    @function
    def build_kotlin_app(self, source: Directory) -> Container:
        """Builds the Kotlin application using Gradle"""
        return (
            dag.container()
            .from_("gradle:8.11.1-jdk21-alpine")
            .with_mounted_directory("/app", source)
            .with_workdir("/app")
            .with_exec(["gradle", "build", "--no-daemon"])
        )

    @function
    async def run_kotlin_tests(self, source: Directory) -> str:
        """Runs the Kotlin tests and returns the output"""
        return await (
            dag.container()
            .from_("gradle:8.11.1-jdk21-alpine")
            .with_mounted_directory("/app", source)
            .with_workdir("/app")
            .with_exec(["gradle", "kotest", "--no-daemon"])
            .stdout()
        )

    @function
    async def build_and_test(self, source: Directory) -> str:
        """Builds the Kotlin application and runs tests, returning test results"""
        # First build the application
        build_container = (
            dag.container()
            .from_("gradle:8.11.1-jdk21-alpine")
            .with_mounted_directory("/app", source)
            .with_workdir("/app")
            .with_exec(["gradle", "build", "--no-daemon"])
        )

        # Then run tests and return output
        return await (
            build_container
            .with_exec(["gradle", "kotest", "--no-daemon"])
            .stdout()
        )
