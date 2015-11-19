/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package edu.ncku.ikdd;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.*;

/**
 *
 * @author ril
 */
public class DataMining {
    
    private static final String count_path = "tmp_count_output/count";
    private static final String candidate_path = "tmp_candidate_output/candidate";
    
    public static List<Integer> string2intList(String line) {
        StringTokenizer tokenizer = new StringTokenizer(line);
        List<Integer> intList = new ArrayList<>();
        while (tokenizer.hasMoreTokens()) {
            intList.add(Integer.valueOf(tokenizer.nextToken()));
        }
        return intList;
        
    }
    
    public static String intList2String(List<Integer> intList) {
        String line = "";
        for (int i = 0; i < intList.size(); ++i) {
            if (i != 0) {
                line += " ";
            }
            line += String.valueOf(intList.get(i));
        }
        return line;
    }
    
    public static class CountMap extends MapReduceBase implements Mapper<LongWritable, Text, Text, IntWritable> {
        private static final IntWritable one = new IntWritable(1);
        private static Text text = new Text();
        private static int candidateLength;
        private BufferedReader br;
        private JobConf conf;

        @Override
        public void map(LongWritable k1, Text v1, OutputCollector<Text, IntWritable> oc, Reporter rprtr) throws IOException {
            String line = v1.toString();
            if (candidateLength == 1) {
                StringTokenizer tokenizer = new StringTokenizer(line);
                while (tokenizer.hasMoreTokens()) {
                    text.set(tokenizer.nextToken());
                    oc.collect(text, one);
                }
            } else {
                List<Integer> tList = DataMining.string2intList(line), cList;
                boolean isIn;
                br = new BufferedReader(
                    new InputStreamReader(
                            FileSystem.get(conf).open(new Path(candidate_path + String.valueOf(candidateLength) + "/part-00000"))
                    )
                );
                while ((line = br.readLine()) != null) {
                    cList = DataMining.string2intList(line);
                    isIn = true;
                    for (Integer i : cList) {
                        if (tList.indexOf(i) == -1) {
                            isIn = false;
                            break;
                        }
                    }
                    if (isIn == false) {
                        continue;
                    }
                    text.set(line);
                    oc.collect(text, one);
                }
                br.close();
            }
        }
        
        public void configure(JobConf job) {
            candidateLength = job.getInt("candidateLength", 1);
            conf = job;
        }
    }
    
    public static class CountCombine extends MapReduceBase implements Reducer<Text, IntWritable, Text, IntWritable> {

        @Override
        public void reduce(Text k2, Iterator<IntWritable> itrtr, OutputCollector<Text, IntWritable> oc, Reporter rprtr) throws IOException {
            int sum = 0;
            while (itrtr.hasNext()) {
                sum += itrtr.next().get();
            }
            oc.collect(k2, new IntWritable(sum));
        }
    }
    
    public static class CountReduce extends MapReduceBase implements Reducer<Text, IntWritable, Text, IntWritable> {
        private static int minSupport;

        @Override
        public void reduce(Text k2, Iterator<IntWritable> itrtr, OutputCollector<Text, IntWritable> oc, Reporter rprtr) throws IOException {
            int sum = 0;
            while (itrtr.hasNext()) {
                sum += itrtr.next().get();
            }
            if (sum >= minSupport) {
                oc.collect(k2, new IntWritable(sum));
            }
        }
        
        public void configure(JobConf job) {
            minSupport = job.getInt("minSupport", 2);
        }
    }
    
    public static class CandidateMap extends MapReduceBase implements Mapper<LongWritable, Text, Text, Text> {
        private static int candidateLength;
        private static final Pattern pattern = Pattern.compile("(.*)\\s\\d+");
        private BufferedReader br;
        private static Text text = new Text();
        private static final Text empty = new Text("");
        private JobConf conf;

        @Override
        public void map(LongWritable k1, Text v1, OutputCollector<Text, Text> oc, Reporter rprtr) throws IOException {
            String line = v1.toString(), summary;
            Matcher matcher = pattern.matcher(line);
            matcher.find();
            summary = matcher.group(1);
            br = new BufferedReader(
                    new InputStreamReader(
                            FileSystem.get(conf).open(new Path(count_path + String.valueOf(candidateLength - 1) + "/part-00000"))
                    )
            );
            while ((line = br.readLine()) != null) {
                matcher = pattern.matcher(line);
                matcher.find();
                List<Integer> intList = join(DataMining.string2intList(summary + " " + matcher.group(1)));
                if (intList.size() == candidateLength) {
                    Collections.sort(intList);
                    text.set(DataMining.intList2String(intList));
                    oc.collect(text, empty);
                }
            }
            br.close();
        }
        
        public void configure(JobConf job) {
            candidateLength = job.getInt("candidateLength", 1);
            conf = job;
        }
        
        private List<Integer> join (List<Integer> l1) {
            Set<Integer> set = new HashSet<>();
            List<Integer> list = new ArrayList<>();
            for (Integer i : l1) {
                set.add(i);
            }
            for (Integer i : set) {
                list.add(i);
            }
            return list;
        }
    }
    
    public static class CandidateReduce extends MapReduceBase implements Reducer<Text, Text, Text, Text> {
        private static final Text empty = new Text("");

        @Override
        public void reduce(Text k2, Iterator<Text> itrtr, OutputCollector<Text, Text> oc, Reporter rprtr) throws IOException {
            oc.collect(k2, empty);
        }
    }
    
    public static class FinalMap extends MapReduceBase implements Mapper<LongWritable, Text, IntWritable, Text> {
        private static final Pattern pattern = Pattern.compile("(.*)\\s(\\d+)");

        @Override
        public void map(LongWritable k1, Text v1, OutputCollector<IntWritable, Text> oc, Reporter rprtr) throws IOException {
            Matcher matcher = pattern.matcher(v1.toString());
            oc.collect(new IntWritable(Integer.valueOf(matcher.group(2))), new Text(matcher.group(1)));
        }
    }
    
    public static class FinalReduce extends MapReduceBase implements Reducer<IntWritable, Text, Text, IntWritable> {

        @Override
        public void reduce(IntWritable k2, Iterator<Text> itrtr, OutputCollector<Text, IntWritable> oc, Reporter rprtr) throws IOException {
            while (itrtr.hasNext()) {
                oc.collect(itrtr.next(), k2);
            }
        }
    }
    
    public static void main(String[] argv) throws Exception {
        int candidateLength = 1;
        FileSystem dfs = FileSystem.get(new Configuration());
        do {
            JobConf countConf = new JobConf(DataMining.class);
            
            countConf.setOutputKeyClass(Text.class);
            countConf.setOutputValueClass(IntWritable.class);
            
            countConf.setMapperClass(CountMap.class);
            countConf.setCombinerClass(CountCombine.class);
            countConf.setReducerClass(CountReduce.class);
            
            countConf.setInputFormat(TextInputFormat.class);
            countConf.setOutputFormat(TextOutputFormat.class);
            
            FileInputFormat.setInputPaths(countConf, new Path(argv[0]));
            FileOutputFormat.setOutputPath(countConf, new Path(count_path + String.valueOf(candidateLength)));
            countConf.setInt("minSupport", Integer.valueOf(argv[2]));
            countConf.setInt("candidateLength", candidateLength);
            JobClient.runJob(countConf);
            
            ++candidateLength;
            
            JobConf candidateConf = new JobConf(DataMining.class);
            
            candidateConf.setOutputKeyClass(Text.class);
            candidateConf.setOutputValueClass(Text.class);
            
            candidateConf.setMapperClass(CandidateMap.class);
            candidateConf.setReducerClass(CandidateReduce.class);
            
            candidateConf.setInputFormat(TextInputFormat.class);
            candidateConf.setOutputFormat(TextOutputFormat.class);
            
            FileInputFormat.setInputPaths(candidateConf, new Path(count_path + String.valueOf(candidateLength - 1) + "/part-00000"));
            FileOutputFormat.setOutputPath(candidateConf, new Path(candidate_path + String.valueOf(candidateLength)));
            candidateConf.setInt("candidateLength", candidateLength);
            
            JobClient.runJob(candidateConf);
            
        } while (dfs.getFileStatus(new Path(candidate_path + String.valueOf(candidateLength) + "/part-00000")).getLen() > 0);
        
        BufferedReader br;
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(dfs.create(new Path(argv[1] + "/part-00000"))));
        String line;
        for (int i = 1; i < candidateLength; ++i) {
            br = new BufferedReader(
                    new InputStreamReader(
                            dfs.open(new Path(count_path + String.valueOf(i) + "/part-00000"))
                    )
            );
            while ((line = br.readLine()) != null) {
                bw.write(line + "\n");
            }
            br.close();
        }
        bw.close();
    }
}

