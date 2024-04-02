//import java.io.BufferedWriter;
//import java.io.FileWriter;
//import java.io.IOException;
import java.time.Duration;
//import java.util.HashSet;
import java.util.List;
//import java.util.Set;

import io.github.bonigarcia.wdm.WebDriverManager;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

public class DataCollector {

    public static void main(String[] args) throws InterruptedException {


        WebDriverManager.chromedriver().setup();
        WebDriver driver = new ChromeDriver();

        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(100));
        driver.manage().timeouts().scriptTimeout(Duration.ofMinutes(20));
        driver.manage().timeouts().pageLoadTimeout(Duration.ofSeconds(40));

        driver.get("https://google.com");
        driver.navigate().to("https://boukiebanane.com/");


//        List<WebElement> links = driver.findElements(By.tagName("a"));
//        Set<String> uniqueLinks = new HashSet<>();


        Thread.sleep(3000);

        List<WebElement> links = driver.findElements(By.xpath("//*[@id=\"gs_bdy_ccl\"]"));
        System.out.println("::".repeat(20));
        System.out.println(links.size());
        System.out.println("::".repeat(20));
//        for (WebElement link : links) {
//            uniqueLinks.add(link.getAttribute("href"));
//        }
//        try (BufferedWriter writer = new BufferedWriter(new FileWriter("DataSet.txt"))) {
//            for (String url : uniqueLinks) {
//                Thread.sleep(2000);
//                driver.navigate().to(url);
//                String pageText = driver.findElement(By.tagName("body")).getText();
//                writer.write("Inhalt von " + url + ":\n" + pageText + "\n\n");
//                writer.write("-------------------------------------------------\n");
//            }
//        } catch (IOException | InterruptedException e) {
//            System.err.println(e);
//        }
        driver.close();
    }
}
