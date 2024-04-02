
# Install Java & Maven
```
sudo apt install openjdk-19-jdk openjdk-19-jre
sudo apt install maven
```


# Build DataCollector
```
cd ./DataCollector
mvn clean install
```
This will generate a JAR file in the target directory.

# Run DataCollector
```
java -jar ./target/DataCollector-1.0-SNAPSHOT.jar
```

# WebDriver
- Chromium Version 123.0.6312.86
→ https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.86/linux64/chromedriver-linux64.zip
(For other versions: https://chromedriver.chromium.org/downloads/version-selection)

- Firefox Version 124.0.1
→ https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz
(For other versions: https://github.com/mozilla/geckodriver/releases)

