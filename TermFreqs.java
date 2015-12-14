import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.TreeMap;


public class TermFreqs {
	static class TermDetails{
		int totCorpusFreq;
		int docCnt;
	}
	
	
	static TreeMap<String, Integer> termsHMSimple = new TreeMap<String, Integer>();
	public static void Sort(String fileName, String SortedInputFileName, HashSet<String> stopWordHS) throws IOException, InterruptedException{
		BufferedReader br = new BufferedReader(new FileReader(fileName));
		String line;
		Map<String, Integer> termsHMSimple = new HashMap<String, Integer>();
		int lineno = 0;
		while((line = br.readLine()) != null){
			String[] term_freq = line.split("\t");
			
			if(stopWordHS.contains(term_freq[0]) || term_freq[0].length() < 3 ) continue;
//			System.out.println(term_freq[0]+"&"+ Integer.parseInt(term_freq[1]));
			termsHMSimple.put(term_freq[0], Integer.parseInt(term_freq[1]));
			lineno++;
			if(lineno % 100000 == 0) {
				System.out.print(".");
				System.out.flush();
			}
		}
		br.close();
		ArrayList<Map.Entry<String, Integer>> entryList = new ArrayList<>(termsHMSimple.entrySet());

		sortByValue(entryList);
		int cnt = 1;
		BufferedWriter bw1 = new BufferedWriter(new FileWriter(SortedInputFileName));
		for (Map.Entry<String, Integer> e : entryList) {
			bw1.write(e.getKey() + " = " + e.getValue()+"\n");
//			System.out.println(e.getKey() + " = " + e.getValue());
			cnt++;
//			if (cnt >= 10000) break;
		}
		bw1.close();
    }
	
	private static void sortByValue(ArrayList<Entry<String, Integer>> entryList) {
		Collections.sort(entryList, new Comparator<Map.Entry<String, Integer>>() {

			@Override
			public int compare(Entry<String, Integer> o1, Entry<String, Integer> o2) {
				// Desc order.
				return o2.getValue().compareTo(o1.getValue());
			}
		});
	}
	
	private static HashSet<String> readStopWordList(String stopWordFileName) throws IOException {
		// TODO Auto-generated method stub
		BufferedReader br = new BufferedReader(new FileReader(stopWordFileName));
		HashSet<String> stopWordsHS = new HashSet<String>();
		String line;
		while((line = br.readLine()) != null){
			stopWordsHS.add(line.trim());
		}
		return stopWordsHS;
	}
	
	public static void main(String args[]) throws IOException, InterruptedException{
		String InputFileName = "/Users/archana/Desktop/PhD/Code/PrivacyAlert/data/MaritalDocTermFreqs_1.json";
		String SortedInputFileName = "/Users/archana/Desktop/PhD/Code/PrivacyAlert/data/MaritalDocTermFreqs_Sorted";
		String StopWordFileName = "/Users/archana/Desktop/PhD/Code/PrivacyAlert/data/stopwords";
		HashSet<String> stopWordHS = readStopWordList(StopWordFileName);
    	Sort(InputFileName, SortedInputFileName, stopWordHS);
	}
}
