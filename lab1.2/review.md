% Лабораторная работа № 1.2. «Лексический анализатор
  на основе регулярных выражений»
% 4 марта 2025 г.
% Шоди Шоимов, ИУ9-62Б

# Цель работы
Целью данной работы является приобретение навыка разработки простейших лексических 
анализаторов, работающих на основе поиска в тексте по образцу, заданному регулярным 
выражением.


# Индивидуальный вариант
Идентификаторы: последовательности буквенных символов Unicode, цифр и дефисов, 
начинающиеся с заглавной буквы.

Директивы: любой знак валюты, после которого следует непустая последовательность 
заглавных букв.

Знаки операций: «(», «)», «<», «>».
# Реализация

```java
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
        new Domain("IDENT", Pattern.compile("\\A\\{Lu}[\\p{L}0-9-]*")),
        new Domain("DIRECT", Pattern.compile("\\A\\{Sc}[A-Z]+")),
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
                        System.out.println(d.name + ": " + word + " (" + index + "," 
+ start + ")");
                        matched = true;   
                    }
                }
                if (!matched) {   
                    System.out.println("Error: No match for word " + word + " (" + index 
+ "," + start + ")");
                }
                start = end;   
            }
            index += 1;
        }
    }
}

```

# Тестирование

Входные данные

```
AAaaaaaa  Hello
< > ( )
$ASB
<> $asdd
$ASB12a
```

Вывод на `stdout` (если необходимо)

```
IDENT: AAaaaaaa (1,1)
IDENT: Hello (1,11)
OPERATOR: < (2,1)
OPERATOR: > (2,3)
OPERATOR: ( (2,5)
OPERATOR: ) (2,7)
DIRECT: $ASB (3,1)
Error: No match for word <> (4,1)
Error: No match for word $asdd (4,4)
DIRECT: $ASB12a (5,1)
```

# Вывод
   В ходе выполнения лабораторной работы я реализовал две первые фазы стадии анализа: 
чтение входного потока и лексический анализ на языке Java. Программа читает входной 
файл в кодировке UTF-8 и вычисляет текущие координаты в обрабатываемом тексте.

  Я углубил свои знания о регулярных выражениях, научившись составлять их для различных 
типов лексем, таких как идентификаторы, числовые литералы, операторы и т.д. Я понял, 
как использовать классы символов Unicode для обозначения букв, чисел и других множеств 
символов. Я научился строить регулярные выражения для каждого домена отдельно, что позволяет 
более точно и гибко обрабатывать входные данные. Я понял, как использовать группы захвата и 
альтернации для создания сложных регулярных выражений.

  Я научился обрабатывать синтаксические ошибки во входном файле и выдавать сообщения с указанием 
координат ошибки. Я реализовал схему восстановления после обнаружения ошибки, пропуская все 
подряд идущие символы до нахождения следующей лексемы.

В ходе изучения регулярных выражений для выполнения лабораторной работы я наткнулся на сайт 
regexcrossword.com. Этот сайт предлагает увлекательные задачи на составление регулярных выражений 
в формате кроссвордов. Я порешал больше половины задач на этом сайте, что заняло около 30 минут. 
Это не только помогло мне лучше понять, как строятся регулярные выражения, но и сделало процесс 
обучения более интересным и увлекательным. Советую!
