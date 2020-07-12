# Travelling Salesman Problem Challenges.
I tried this problem when I joined [Build@Mercari 2020](https://mercan.mercari.com/articles/19631/) Week4.    
This is forked from [https://github.com/mercari-build/week4-tsp](https://github.com/mercari-build/week4-tsp).   
My score was the shortest distance recorded in this program:sparkles:   

## Demo
![tsp](https://user-images.githubusercontent.com/56245555/87240480-e5356480-c454-11ea-9c64-ab2175e60899.gif)
## How to use a visualizer
0. Go to this [link](https://harunamarun.github.io/week4-tsp/visualizer/
), if you want to just see the result of a fast solver.   

1. Open `solution_generator.py` and change file which you want to run.(`line20`)  
I implemented multiple solutions.
The default file is `solver_1.py` which is my best solution, but it needs a long time.   
I used 24 CPU in Google Cloud Platform and the run time is one day:joy:    
Because of that if you want to try `solver_1`, I recommend adjust some parameters such as a beam search width.
```
• solver_1   
• solver_using_nn   
• solver_using_chi   
```

2. Create outputs file.
```
python3 solution_generator.jp
```
3. Run the server and go to this link. 
```
./nocache_server.py
```
[`http://localhost:8000/visualizer/`](http://localhost:8000/visualizer/)


## Algorithm
### Approximation algorithm
- Nearest Neighbor   
- Convex Hull Insertion   
### Improvement algorithm
- 2-opt   
- Or-opt   

## Originality
- multi processing   
- Beam Search   
- Randomness in Nearest Neighbor Algorithm. Sometimes choose the second nearest city.

## Evaluation
NN ••• Nearest Neighbor   
CHI ••• Convex Hull Insertion   

|                                                 | N = 5   | N = 8   | N = 16  | N = 64  | N = 128  | N = 512  | N = 2048 | file name |
| ----                                            | ----    | ----    | ----    | ----    | ----     | ----     | ----     | ----      |
| NN                                              | 3418.10 | 3832.29 | 5065.58 | 9276.22 | 12084.32 | 24191.66 | 47822.41 | -         |
| NN + loop(2-opt)                                | 3291.62 | 3778.72 | 4494.42 | 8177.54 | 10646.62 | 20445.66 |  -       | -         |
| NN + loop(2-opt + Or-opt)                       | 3291.62 | 3778.72 | 4494.42 | 8177.54 | 10575.65 | 20360.85 | 40630.57 | solver_using_nn.py |
| CHI + loop(2-opt + Or-opt)                      | 3291.62 | 3778.72 | 4494.42 | 8461.06 | 10840.90 | 21200.09 | 42381.31 | solver_using_chi.py |
| [NN + loop(2-opt + Or-opt) + BeamSearch + random](https://harunamarun.github.io/week4-tsp/visualizer/) | 3291.62 | 3778.72 | 4494.42 | 8118.40 | 10496.039 | 20193.15 | 40476.42 | solver_1.py |   

#### Points of attention
+ Repeat 2-opt + Or-opt until there is no improvement.   
+ Tried Or-opt's with 19 subpath at most.  
+ As for Nearest Neighbor, path depends on the start city. So, I tried starting from all the cities.   
   
## Reference   
[巡回セールスマン問題の近似アルゴリズムについて](https://mie-u.repo.nii.ac.jp/?action=repository_action_common_download&item_id=5071&item_no=1&attribute_id=17&file_no=1)   
[巡回セールスマン問題における局所探索法の提案](https://www.cst.nihon-u.ac.jp/research/gakujutu/57/pdf/L-20.pdf)   
[Algorithms with Python](http://www.nct9.ne.jp/m_hiroi/light/pyalgo23.html)    
   
   
   
----
----

Build@Mercari 2020 Week4 - Travelling Salesman PRoblem Challenges.

This is forked from [https://github.com/hayatoito/google-step-tsp-2016](https://github.com/hayatoito/google-step-tsp-2016).

1. 問題
[巡回セールスマン問題](https://ja.wikipedia.org/wiki/%E5%B7%A1%E5%9B%9E%E3%82%BB%E3%83%BC%E3%83%AB%E3%82%B9%E3%83%9E%E3%83%B3%E5%95%8F%E9%A1%8C) を解くアルゴリズムを考えてください。

2. 課題
----
このrepositoryを自分のgithubにforkして使ってください。
N = 5 から N = 2048までの７つの課題があります。

| Challenge    | N (= the number of cities) | Input file  | Output (Solution) file |
| ------------ | -------------------------: | ----------- | ---------------------- |
| Challenge 0  |                          5 | input_0.csv | solution_yours_0.csv   |
| Challenge 1  |                          8 | input_1.csv | solution_yours_1.csv   |
| Challenge 2  |                         16 | input_2.csv | solution_yours_2.csv   |
| Challenge 3  |                         64 | input_3.csv | solution_yours_3.csv   |
| Challenge 4  |                        128 | input_4.csv | solution_yours_4.csv   |
| Challenge 5  |                        512 | input_5.csv | solution_yours_5.csv   |
| Challenge 6  |                       2048 | input_6.csv | solution_yours_6.csv   |

inputとoutputの形式については *3. Data Format Specification* を見てください。
### Your tasks

* 巡回セールスマン問題をとくアルゴリズムを考えて実装してください。
* `solution_yours_{0-6}.csv` をあなたのアルゴリズムでといた結果で上書きしてください。
* あなたの解法の*path length*を[scoreboard]に書いてください

[scoreboard]: https://docs.google.com/spreadsheets/d/1t4ScULZ7aZpDJL8i9AVFQfqL7sErjT5i3cmC1G5ecR8/edit?usp=sharing
### An optional task (Speed challenge)

What matters in this optional task is your program's *speed* (execution time). The path length does not matter as long as it meets the condition.
Your task is:

* Given `input_6.csv`, write a program which outputs a path shorter than `47,000`

Input your program's execution time in the [scoreboard]. Faster (smaller) is better.

You can measure the execution time by `time` command.

```shellsession
$ time yourprogram input_6.csv solution_yours_6.csv
2.96s user 0.07s system 97% cpu 3.116 total
```

In this case, your score is `3.116` (s).

### Visualizer

The demo page of the visualizer is:
https://mercari-build.github.io/week4-tsp/visualizer/.

The assignment includes a helper Web page, `visualizer/index.html`, which
visualizes your solutions. You need to run a HTTP server on your local machine
to access the visualizer. Any HTTP server is okay. If you are not sure how to
run a web server, use the following command to run the HTTP server included in
the assignment. Make sure that you are in the top directory of the assignment
before running the command.

``` shellsession
./nocache_server.py # For Python 3
./nocache_server.py2.py # If you don’t want to install Python3
```

Then, open a browser and navigate to the
[http://localhost:8000/visualizer/](http://localhost:8000/visualizer/). Note
that visualizer was only tested by Google Chrome.  Using the visualizer is
up-to you. You don’t have to use the visualizer to finish the assignment. The
visualizer is provided for the purpose of helping you understand the problem.

3. Data Format Specification
----

### Input Format

The input consists of `N + 1` lines. The first line is always `x,y`. It is followed by `N` lines, each line represents an i-th city’s location, point `xi,yi` where `xi`, `yi` is a floating point number.

```
x,y
x_0,y_0
x_1,y_1
…
x_N-1,y_N-1
```

### Output Format

Output has `N + 1` lines. The first line should be “index”. It is followed by `N` lines, each line is the index of city, which represents the visitation order.

```
index
v_0
v_1
v_2
…
v_N-1
```

### Example (Challenge 0, N = 5)

Input Example:

```
x,y
214.98279057984195,762.6903632435094
1222.0393903625825,229.56212316547953
792.6961393471055,404.5419583098643
1042.5487563564207,709.8510160219619
150.17533883877582,25.512728869805677
```

Output (Solution) Example:

```
index
0
2
3
1
4
```

These formats are requirements for the visualizer, which can take only properly formatted CSV files as input.

5. What’s included in the assignment
----

To help you understand the problem, there are some sample scripts / resources
in the assignment, including, but not limited to:

- `solver_random.py` - Sample stupid solver. You never lose to this stupid one.
- `solution_random_{0-6}.csv` - Sample solutions by solver_random.py.
- `solver_greedy.py` - Sample solver using the greedy algorithm. You should beat this definitely.
- `solution_greedy_{0-6}.csv` - Sample solutions by solver_greedy.py.
- `solution_sa_{0-6}.csv` - Yet another sample solutions. I expect all of you will beat this one too. The solver itself is not included intentionally.
- `solution_wakanapo_{0-6}.csv` - Sample solutions I solved when I was joined Google STEP 2016.
- `solution_yours_{0-6}.csv` - You should overwrite these files with your solution.
- `solution_verifier.py` - Try to validate your solution and print the path length.
- `input_generator.py` - Python script which was used to create input files, `input_{0-6}.csv`
- `visualizer/` - The directory for visualizer.

6. Acknowledgments
----
この課題は[私](https://github.com/wakanapo)がgoogle step 2016に参加したときにやったものです。問題のわかりやすさ、visualizerによるアルゴリズムのみやすさ、楽しさなどにおいてこれを上回る課題はないと思ったので、Build@Mercariでも採用することにしました。
