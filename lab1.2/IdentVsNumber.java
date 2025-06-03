import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Stream;

 
 

public class IdentVsNumber
{
    static int index = 1;

    public static void main(String args[])
    {
        String filePath = "/Users/husravi_qubodioni/Desktop/Compiletor/lab3/test.txt";
        try (Stream<String> stream = Files.lines(Paths.get(filePath))) {
            stream.forEach(IdentVsNumber::test_match);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public record Domain(String name, Pattern pattern) {};

     
    static Domain[] DOMAINS = {
        new Domain("IDENT", Pattern.compile("\\A\\p{Lu}[\\p{L}0-9-]*")),
        new Domain("DIRECT", Pattern.compile("\\A\\p{Sc}[A-Z]+")),
        new Domain("OPERATOR", Pattern.compile("^[()<>]$")),
        new Domain("NEWLINE", Pattern.compile("^[\r\n]"))  
    };

    public static void test_match(String text) {
        Matcher newline = DOMAINS[3].pattern.matcher(text);
        if (newline.find()) {  
            System.out.println("NEWLINE: " + text.trim());
        } else {
            String[] words = text.trim().split("\\s+");   
            int start = 0;

            for (String word : words) {
                start = text.indexOf(word, start) + 1;   
                int end = start + word.length();     
                boolean matched = false;   

                for (Domain d : DOMAINS) {   
                    Matcher m = d.pattern.matcher(word);
                    if (m.find()) {   
                        System.out.println(d.name + ": " + word + " (" + index + "," + start + ")");
                        matched = true;   
                    }
                }
                if (!matched) {   
                    System.out.println("Error: No match for word " + word + " (" + index + "," + start + ")");
                }
                start = end;   
            }
            index += 1;
        }
    }
}
