public class ReadFile {
    public static void main(String[] args) {
        String str = "hello      my name is    SSSSSS";

        // Split the string by one or more spaces
        String[] words = str.trim().split("\\s+");

        int start = 0; // Initialize the starting position of the string
        for (String word : words) {
            // Find the start index by checking where the word is located in the original string
            start = str.indexOf(word, start); // The second parameter ensures we search from the current position onwards
            
            // Calculate the end index (start index + word length)
            int end = start + word.length() - 1;

            // Output the word and its positions
            System.out.println(word + "(" + start + "," + end + ")");
            
            // Move the start position for the next word
            start = end + 1;
        }
    }
}
