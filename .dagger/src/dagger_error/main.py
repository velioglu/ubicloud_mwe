from dagger import dag, function, object_type, Container, Directory

@object_type
class DaggerError:
    @function
    def build_kotlin_app(self, source: Directory) -> Container:
        """Builds the Kotlin application using Gradle"""
        return (
            dag.container()
            .from_("openjdk:21-jdk-alpine")
            .with_mounted_directory("/app", source)
            .with_workdir("/app")
            .with_exec(["./gradlew", "build", "--no-daemon"])
        )

    @function
    async def run_kotlin_tests(self, source: Directory) -> str:
        """Runs the Kotlin tests and returns the output"""
        return await (
            dag.container()
            .from_("openjdk:21-jdk-alpine")
            .with_mounted_directory("/app", source)
            .with_workdir("/app")
            .with_exec(["./gradlew", "test", "--no-daemon"])
            .stdout()
        )

    @function
    async def build_and_test(self, source: Directory) -> str:
        """Builds the Kotlin application and runs tests, returning test results"""
        # First build the application
        build_container = (
            dag.container()
            .from_("openjdk:17-jdk-alpine")
            .with_mounted_directory("/app", source)
            .with_workdir("/app")
            .with_exec(["./gradlew", "build", "--no-daemon"])
        )

        # Then run tests and return output
        return await (
            build_container
            .with_exec(["./gradlew", "test", "--no-daemon"])
            .stdout()
        )

    @function
    def container_echo(self, string_arg: str) -> Container:
        """Returns a container that echoes whatever string argument is provided"""
        return dag.container().from_("alpine:latest").with_exec(["echo", string_arg])

    @function
    async def grep_dir(self, directory_arg: Directory, pattern: str) -> str:
        """Returns lines that match a pattern in the files of the provided Directory"""
        return await (
            dag.container()
            .from_("alpine:latest")
            .with_mounted_directory("/mnt", directory_arg)
            .with_workdir("/mnt")
            .with_exec(["grep", "-R", pattern, "."])
            .stdout()
        )
