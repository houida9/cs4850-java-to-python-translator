public class NestedIfAndLoops
{
    public static void main(String args[])
    {
        int time = 55;
        int i = 0;
        if (time < 10) {
            for(int i = 0; i < 3; i++){
                System.out.println("Good day.");
            }
        } else if (time > 100) {
            for(int i = 0; i <= 3; i++){
                for(int i = 0; i <= 3; i++){
                    System.out.println("Good evening.");
                    }
            }
        }else{
            while(i <= 3){
                while( i < 3){
                    System.out.println("Good Bye");
                    i++;
                }
            }
        }
    }
}