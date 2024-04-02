import com.opencsv.CSVWriter;
import io.github.bonigarcia.wdm.WebDriverManager;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

import java.awt.*;
import java.io.FileWriter;
import java.io.IOException;
import java.time.Duration;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Random;

public class GoogleScholarCollector {

    public static void main(String[] args) throws InterruptedException, AWTException {
        GoogleScholarCollector googleScholarCollector = new GoogleScholarCollector();
        Random random = new Random();
        WebDriverManager.chromedriver().setup();
        WebDriver driver = new ChromeDriver();

        // implicitWait means: TODO
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(100));
        // scriptTimeout happens when: TODO  &  NOTE: We use minutes instead of seconds because:
        driver.manage().timeouts().scriptTimeout(Duration.ofMinutes(5));
        // pageLoadTimeout happens when: TODO
        driver.manage().timeouts().pageLoadTimeout(Duration.ofSeconds(100));

        driver.get(Literal.GOOGLE_URL);
        driver.navigate().to(Literal.GOOGLE_SCHOLAR);
        Thread.sleep(3000 + random.nextInt(5000));
        googleScholarCollector.doCrawling(driver);
        Thread.sleep(3000 + random.nextInt(5000));
    }


    public void doCrawling(WebDriver driver) throws InterruptedException {
        Random random = new Random();
        driver.findElement(By.xpath("//input[@name='q']")).sendKeys(Literal.QUERY);
        Thread.sleep(3000 + random.nextInt(5000));
        driver.findElement(By.xpath("//button[@name='btnG']")).click();
        Thread.sleep(3000 + random.nextInt(2000));
        try (CSVWriter writer = new CSVWriter(new FileWriter("output-data-" + LocalTime.now().format(DateTimeFormatter.ofPattern("HHmm")) + ".csv"))) {
            writer.writeNext(new String[]{"Topic", "TitleText", "TitleLink", "PDFText", "PDFLink", "AbstractText", "AuthorText"});
            //writer.writeNext(new String[]{"hauptTitelText", "HauptTitelAlsLink"});

            doRead(writer, driver);
            List<WebElement> nextButton = driver.findElements(By.xpath("//div[@class='gs_r gs_alrt_btm gs_oph gs_ota']/..//a[contains(., 'Weiter')]/../a"));
            if (nextButton.size() != 0) {
                for (int i = 0; i <= 2; i++) {
                    driver.findElement(By.xpath("//div[@class='gs_r gs_alrt_btm gs_oph gs_ota']/..//a[contains(., 'Weiter')]/../a")).click();
                    doRead(writer, driver);
                    Thread.sleep(3000 + random.nextInt(1000));
                }
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private void doRead(CSVWriter writer, WebDriver driver) throws InterruptedException {
        List<WebElement> titel = driver.findElements(By.xpath("//div[@class='gs_ri']/h3/a"));
        for (int i = 1; i < titel.size() + 1; i++) {
            Thread.sleep(3000);
            List<WebElement> titleTextList = driver.findElements(By.xpath("(//div[@class='gs_ri'])[" + i + "]/h3/a"));
            List<WebElement> titleLinkList = driver.findElements(By.xpath("(//div[@class='gs_ri'])[" + i + "]/h3/a"));
            List<WebElement> pdfTextList = driver.findElements(By.xpath("(//div[@class='gs_ri'])[" + i + "]/h3/a/../../..//a[contains(., 'PDF')]"));
            List<WebElement> pdfLinkList = driver.findElements(By.xpath("(//div[@class='gs_ri'])[" + i + "]/h3/a/../../..//a[contains(., 'PDF')]"));
            List<WebElement> abstractTextList = driver.findElements(By.xpath("(//div[@class='gs_ri'])[" + i + "]/div[@class='gs_rs']"));
            List<WebElement> authorTextList = driver.findElements(By.xpath("(//div[@class='gs_ri'])[" + i + "]/h3/..//div[@class='gs_a']"));


            Thread.sleep(3000);
            String hauptTitelTextString = "";
            String hauptTitelLinkString = "";
            String hauptTitelExtendPDFString;
            String hauptTitelExtendPDFLinkString;
            String beschreibungTextString = "";
            String authorString = "";
            if (titleTextList.size() != 0) {
                hauptTitelTextString = titleTextList.get(0).getText();
            }
            if (titleLinkList.size() != 0) {
                hauptTitelLinkString = titleLinkList.get(0).getAttribute("href");
            }
            if (pdfTextList.size() != 0) {
                hauptTitelExtendPDFString = pdfTextList.get(0).getText();
            }else {
                hauptTitelExtendPDFString = " ";
            }
            if (pdfLinkList.size() != 0) {
                hauptTitelExtendPDFLinkString = pdfLinkList.get(0).getAttribute("href");
            }else {
                hauptTitelExtendPDFLinkString = " ";
            }
            if (abstractTextList.size() != 0) {
                beschreibungTextString = abstractTextList.get(0).getText();
            }
            if (authorTextList.size() != 0) {
                int hyphenIndex = authorTextList.get(0).getText().indexOf("-");
                authorString = hyphenIndex != -1 ? authorTextList.get(0).getText().substring(0, hyphenIndex).trim() : "Author not found";
            }
            Thread.sleep(3000);
            writer.writeNext(new String[]{Literal.QUERY,
                    hauptTitelTextString,
                    hauptTitelLinkString,
                    hauptTitelExtendPDFString,
                    hauptTitelExtendPDFLinkString,
                    beschreibungTextString,
                    authorString});

            if (titleTextList.size() != 0) {
                titleTextList.remove(0);
            }
            if (titleLinkList.size() != 0) {
                titleLinkList.remove(0);
            }
            if (pdfTextList.size() != 0) {
                pdfTextList.remove(0);
            }
            if (pdfLinkList.size() != 0) {
                pdfLinkList.remove(0);
            }
            if (abstractTextList.size() != 0) {
                abstractTextList.remove(0);
            }
            if (authorTextList.size() != 0) {
                authorTextList.remove(0);
            }
            Thread.sleep(4000);
        }
    }

}
