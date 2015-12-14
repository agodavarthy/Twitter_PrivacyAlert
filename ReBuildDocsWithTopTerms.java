import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashSet;

import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.Terms;
import org.apache.lucene.index.TermsEnum;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.BytesRef;
import org.json.simple.JSONObject;

public class ReBuildDocsWithTopTerms {

    private static HashSet<String> buildTopTermsSet(File topTermFreqFilePath) throws IOException {
    	BufferedReader br = new BufferedReader(new FileReader(topTermFreqFilePath));
    	String line = "";
    	HashSet<String> termsHS = new HashSet<String>();
    	while((line = br.readLine()) != null){
    		String term = line.split(" = ")[0];
    		termsHS.add(term);
    	}
    	br.close();
    	return termsHS;
   	}
    
	private static void iterate_through_docs(HashSet<String> termsHS, File outputFile, DirectoryReader ireader) throws IOException {
    	BufferedWriter bw = new BufferedWriter(new FileWriter(outputFile));
    	int posCnt = 0, negCnt = 0;
		for (int i = 0; i < ireader.maxDoc(); i++){
			String user_id = ireader.document(i).get("user_id");
			String target_id = ireader.document(i).get("target_id");
			String target_name = ireader.document(i).get("target_name");
			System.out.println(ireader.document(i).get("target_id"));
			System.out.println(ireader.document(i).get("target_name"));
    		if(target_id.equals("0")) negCnt++;
    		else if(target_id.equals("1")) posCnt++;
			Terms vector = ireader.getTermVector(i, "content");	
		    if (vector != null){
		    	StringBuffer sb = new StringBuffer();
				TermsEnum termsEnum = null;
					termsEnum = vector.iterator(termsEnum);
					for(String term : termsHS){
						try{
							BytesRef term_bytesref = new BytesRef(term);
				    		if (termsEnum.seekExact(term_bytesref, true)){
				    			int termFreq = (int) termsEnum.totalTermFreq();
//				    			System.out.println(term+" "+ termFreq);
				    			for(int j = 0; j < termFreq; j++){
				    				sb.append(term+" ");
				    			}
				    		}
						}catch(IllegalArgumentException e){
							continue;
						}
				   }
//				   bw.write(sb.toString()+"\n");
				   String tweet_doc = sb.toString();
				   JSONObject jsonObj = new JSONObject();
				   jsonObj.put("user_id", user_id);
				   jsonObj.put("target_id", target_id);
				   jsonObj.put("target_name", target_name);
				   jsonObj.put("tweet_doc", tweet_doc);
				   bw.write(jsonObj.toJSONString()+"\n");
				   System.out.println("************* "+i+" ***********");
//				   System.exit(1);
		    }
    	}
		bw.close();
	}

    private static void buildDocuments_v2(File luceneIndexFilePath, HashSet<String> termsHS, File outputFile) throws Exception{
        DirectoryReader ireader = null;
        Directory directory = null;
        directory = FSDirectory.open(luceneIndexFilePath);
        ireader = DirectoryReader.open(directory);
        iterate_through_docs(termsHS, outputFile, ireader);
    }

	public static void main(String args[]) throws Exception{
//		String LuceneIndexFileName = "MaritalProcessedAllFull_EnglishAnalyzer";
		String LuceneIndexFileName = "MaritalProcessedAllFull_Dec12_StandardAnalyzer/";
		String filePathStr = "/Users/archana/Desktop/PhD/Code/PrivacyAlert/data/LuceneIndexes/";
		String luceneIndexPathStr = filePathStr+LuceneIndexFileName;
    	File luceneIndexFilePath = new File(luceneIndexPathStr);
    	int topFreqCnt = 10000;
    	String topFreqCntStr = "10k";
    	String fileName = "MaritalProcessedAllFull_Dec12_StandardAnalyzer_Top"+topFreqCntStr+".txt";
    	String TopTermsDOCs_output_fileName = "/Users/archana/Desktop/PhD/Code/PrivacyAlert/data/CurrentProcessingFiles/FinalProductionFiles/"+fileName;
    	String TopTermFreqFileName = "/Users/archana/Desktop/PhD/Code/PrivacyAlert/data/CurrentProcessingFiles/FinalProductionFiles/MaritalDocTermFreqs_"+topFreqCntStr;
    	File TopTermFreqFilePath = new File(TopTermFreqFileName);
    	File TopTermsDOCs_output_filePath = new File(TopTermsDOCs_output_fileName);
    	
    	HashSet<String> termsHS = buildTopTermsSet(TopTermFreqFilePath);
    	buildDocuments_v2(luceneIndexFilePath, termsHS, TopTermsDOCs_output_filePath);
	}
}
