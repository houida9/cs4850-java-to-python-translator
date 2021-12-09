import java.util.Scanner;

public class FactorialandSquare
{
    static int factorial(int n){
        int res = 1;
        for (int i=2; i<=n; i++){
             res *= i;
        }
        return res;
    }
    double square(int n){
        return n * n;
    }

    public static void main(String args[])
    {
        //Prints 0-100 factorial to the screen
        final int NUM_FACTS = 100;
        for(int i = 0; i <= NUM_FACTS; i++){
            System.out.println(i + "i factorial is: " + factorial(i));
        }

        //Prints 0-10 numbers squared
        int z = 0;
        boolean x = true;
        while(x){
            if (z <= 10){
                System.out.println(z + " squared is: " + square(z));
                z++;
            } else {
                x = false;
            }
        }

        //Gets user's input to square the number that they choose
        int userInput;
        while(userInput != 0){
            System.out.println("\nEnter a number you would like to square\nIf you would like to exit type 0 because everyone knows zero squared is zero.\nEnter: ");
            userInput = in.nextInt();
            if (userInput == 0){
                System.out.println("You chose to stop squaring numbers, goodbye! ");
            } else {
                System.out.println(userInput + " squared is " + square(userInput));
            }
        }
    }
}


class helloWorld{
    System.out.println("Hello World");
}
