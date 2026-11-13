plugins {
    kotlin("jvm") version "1.8.0"
    application
    id("com.google.protobuf") version "0.9.2"
}

group = "me.marka"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    testImplementation(kotlin("test"))
    implementation("com.google.protobuf:protobuf-java:3.22.2")
    implementation("com.google.protobuf:protobuf-kotlin:3.22.2")
}

tasks.test {
    useJUnitPlatform()
}

kotlin {
    jvmToolchain(8)
}

application {
    mainClass.set("MainKt")
}

tasks.getByName("run", JavaExec::class) {
    standardInput = System.`in`
}
