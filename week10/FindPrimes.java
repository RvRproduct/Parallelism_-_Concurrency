
/************************************
Course: cse 251
File: team1.java
Week: week 11 - team activity 1
Instructions:
- Main contains an array of 1,000 random values.  You will be creating
  threads to process this array.  If you find a prime number, display
  it to the console.
- DON'T copy/slice the array in main() for each thread.
Part 1:
- Create a class that is a sub-class of Thread.
- create 4 threads based on this class you created.
- Divide the array among the threads.
Part 2:
- Create a class on an interface or Runnable
- create 4 threads based on this class you created.
- Divide the array among the threads.
Part 3:
- Modify part1 or part 2 to handle any size array and any number
  of threads.
************************************/
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

class FindPrimeThread extends Thread {
    List<Integer> numbers;
    List<Integer> primes = Collections.synchronizedList(new ArrayList<Integer>());

    public FindPrimeThread(List<Integer> numbers, List<Integer> primes) {
        this.numbers = numbers;
        this.primes = primes;
    }

    @Override
    public void run() {
        System.out.println("Thread " + Thread.currentThread().getId() + " is running");
        for (Integer number : numbers)
            if (FindPrimes.isPrime(number))
                primes.add(number);
    }
}

class FindPrimes {

    static int MAX_THREADS = 16;

    public static boolean isPrime(int n) {
        // Corner cases
        if (n <= 1)
            return false;
        if (n <= 3)
            return true;

        // This is checked so that we can skip
        // middle five numbers in below loop
        if (n % 2 == 0 || n % 3 == 0)
            return false;

        for (int i = 5; i * i <= n; i = i + 6)
            if (n % i == 0 || n % (i + 2) == 0)
                return false;

        return true;
    }

    public static void main(String[] args) {

        // create instance of Random class
        Random rand = new Random();

        int count = 1000;
        List<Integer> numbers = new ArrayList<>();
        for (int i = 0; i < count; i++) {
            numbers.add(Math.abs(rand.nextInt()));
        }

        // PART 1

        // create a thread safe list to store the prime numbers found
        List<Integer> primes = Collections.synchronizedList(new ArrayList<>());

        // list of our threads
        ArrayList<FindPrimeThread> threads = new ArrayList<>();

        // how big each sub-array should be for each thread to search over
        int partitionSize = (int)Math.ceil(count / MAX_THREADS);

        //System.out.println(String.format("partition size=%s, remainder=%s", partitionSize, remainder));

        for (int i = 0; i < count; i += partitionSize) {

            int start = i;
            int end = start + partitionSize - 1;

            // if we are on the last pass, then set the partitionSize
            // equal to the remainder so that we only get the remaining numbers
            if(end + partitionSize > count) {
                end = count - 1;
                i = count; // to end the loop
            }

            //System.out.println(String.format("start=%s, end=%s", start, end));
            List<Integer> subList = numbers.subList(start, end);

            FindPrimeThread thread = new FindPrimeThread(subList, primes);
            thread.start();
            threads.add(thread);
        }

        for (FindPrimeThread thread : threads) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        Collections.sort(primes);
        for (Integer prime : primes)
            System.out.println("primes = " + prime);
    }
}