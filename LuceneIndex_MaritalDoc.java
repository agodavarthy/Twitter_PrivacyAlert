import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;
import java.security.Timestamp;
import java.text.Normalizer;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpressionException;
import javax.xml.xpath.XPathFactory;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.en.EnglishAnalyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.FieldType;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.Terms;
import org.apache.lucene.index.TermsEnum;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.BytesRef;
import org.apache.lucene.util.Version;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import org.w3c.dom.Node;
//import org.json.simple.JSONObject;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

public class LuceneIndex_MaritalDoc{
	private static Directory directory;
	private static IndexWriterConfig config;
	private static IndexWriter iwriter;
	public static final FieldType TYPE_STORED = new FieldType();
    static {
        TYPE_STORED.setIndexed(true);
        TYPE_STORED.setStored(true);
        TYPE_STORED.setStoreTermVectors(true);
        TYPE_STORED.tokenized();
        TYPE_STORED.storeTermVectorPayloads();
        TYPE_STORED.storeTermVectors();
    }
	public static final FieldType TYPE_STORED_UNANALYZED = new FieldType();
    static {
//    	TYPE_STORED_UNANALYZED.setIndexed(true);
    	TYPE_STORED_UNANALYZED.setStored(true);
//    	TYPE_STORED_UNANALYZED.setStoreTermVectors(true);
    }

    public static void readIndex(File path, String docContent) throws IOException{
    	Directory directory = FSDirectory.open(path);
    	DirectoryReader ireader = DirectoryReader.open(directory);
    	System.out.println("The number of documents is " + ireader.maxDoc());
//    	System.exit(1);
    	for (int i = 0; i < ireader.maxDoc(); i++){
    		Document doc = ireader.document(i);
    		String user_id = doc.get("user_id");
    		String target_id = doc.get("target_id");
    		String target_name = doc.get("target_name");
    		System.out.println(i+" "+target_id+" "+target_name);
//    		Set<String> terms = new HashSet<String>();
//    		Terms vector = ireader.getTermVector(i, docContent);	
//    	    if (vector != null){
//    			TermsEnum termsEnum = null;
//  				termsEnum = vector.iterator(termsEnum);
//   				BytesRef name = null;
//   				while ((name = termsEnum.next()) != null) {
//   					String term = name.utf8ToString();
//   					int freq = (int) termsEnum.totalTermFreq();
//   					terms.add(term);
//   					System.out.print(term + ":" + freq + " ");
//   				}
//   	       } else {
////   	    	   System.out.println("vector is null");
//   	       }
//    	       System.out.println("*****************************");
    	   }
    }
    public static boolean isYear(String pub_year){
    	String patternString = "(([1-9][0-9][0-9][0-9]))";
        Pattern pattern = Pattern.compile(patternString);
        Matcher matcher = pattern.matcher(pub_year);
        boolean matches = matcher.find();
        return matches;
    }

    static class LuceneIndexingObject{
    	String user_id;
    	String content;
    	String target_id;
    	String target_name;
    }
    private static void indexTRECDocuments(LuceneIndexingObject lucIndObj, String indexPath, String luceneAnalyzer) throws IOException{
    	Analyzer analyzer = null;
    	if (luceneAnalyzer.equals("English")){
    		analyzer = new EnglishAnalyzer(Version.LUCENE_43);
    	} else if (luceneAnalyzer.equals("Standard")){
    		analyzer = new StandardAnalyzer(Version.LUCENE_43);
    	}
        File path = new File(indexPath);
        directory = FSDirectory.open(path);
        config = new IndexWriterConfig(Version.LUCENE_43, analyzer);

        iwriter = new IndexWriter(directory, config);

        Document docT = new Document();
        Field field1 = new Field("_id", lucIndObj.user_id, TYPE_STORED);
        Field field2 = new Field("user_id", lucIndObj.user_id, TYPE_STORED);
        Field field3 = new Field("content", lucIndObj.content, TYPE_STORED);
        Field field4 = new Field("target_id", lucIndObj.target_id, TYPE_STORED);
        Field field5 = new Field("target_name", lucIndObj.target_name, TYPE_STORED);

        docT.add(field1);
        docT.add(field2);
        docT.add(field3);
        docT.add(field4);
        docT.add(field5);
        iwriter.addDocument(docT);
        iwriter.close();
}

    public static void iterateFiles_CreateTREC(String inputFile, String luceneIndexPath, String luceneAnalyzer) throws  IOException, InterruptedException, ParseException{
     		BufferedReader br = new BufferedReader(new FileReader(inputFile));
     		String line;
     		JSONParser jParser = new JSONParser();
     		LuceneIndexingObject lucIndObj = new LuceneIndexingObject();
            while((line = br.readLine()) != null) {
            	System.out.println(line);
                JSONObject jObj = (JSONObject) jParser.parse(line);
                String user_id = (String) jObj.get("user_id");
                String content = (String) jObj.get("tweet_doc");
                Object target_id_obj = jObj.get("target_id");
                String target_id = target_id_obj.toString();
                String target_name = (String) jObj.get("target_name");
                lucIndObj.user_id = user_id;
                lucIndObj.content = content;
                lucIndObj.target_id = target_id;
                lucIndObj.target_name = target_name;
                indexTRECDocuments(lucIndObj, luceneIndexPath, luceneAnalyzer);
            }   
    }


	public static String date_ts(){
		java.util.Date date= new java.util.Date();
		String[] date_str = date.toString().split(" |:");
		String date_str_join = "";
		for(String str: date_str){
			date_str_join += "_";
			date_str_join += str;
		}
		return date_str_join;
    }
	

	public static void printHM(Map<String, Float> map) throws IOException {
		for (Map.Entry<String, Float> entry : map.entrySet()) {
			System.out.println(entry.getKey() 
                                      + " : " + entry.getValue());
//			bw.write("Key : " + entry.getKey()  + " Value : " + entry.getValue()+"\n");
		}
	}
	public static void main(String argv[]) throws XPathExpressionException, ParserConfigurationException, SAXException, IOException, InterruptedException, ParseException {
		String inputFileName = "toyKuchipudiPos.json";
		String inputFile ="/Users/archana/Desktop/PhD/Code/PrivacyAlert/data/CurrentProcessingFiles/FinalProductionFiles/preFiles/"+inputFileName;
		String LuceneIndexFileName = "toyKuchipudiPos_StandardAnalyzer";
		String luceneIndexPath = "/Users/archana/Desktop/PhD/Code/PrivacyAlert/data/LuceneIndexes/"+LuceneIndexFileName;
		String luceneAnalyzer = "Standard";
		
    	iterateFiles_CreateTREC(inputFile, luceneIndexPath, luceneAnalyzer);

//    	File luceneIndexFilePath = new File(luceneIndexPath);
//    	readIndex(luceneIndexFilePath, "user_id");
	}
}
  