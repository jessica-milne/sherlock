# -*- coding: utf-8 -*-

from nltk import RegexpParser
from textblob import TextBlob, Word
import re

stopwords = ["a", "a's", "able", "about", "above", "according", "accordingly", "across", "actually", "after", "afterwards",\
			 "again", "against", "ain't", "all", "allow", "allows", "almost", "alone", "along", "already", "also", "although", \
			 "always", "am", "among", "amongst", "an", "and", "another", "any", "anybody", "anyhow", "anyone", "anything", "anyway", \
			 "anyways", "anywhere", "apart", "appear", "appreciate", "appropriate", "are", "aren't", "around", "as", "aside", "ask", \
			 "asking", "associated", "at", "available", "away", "awfully", "b", "be", "became", "because", "become", "becomes", "becoming", \
			 "been", "before", "beforehand", "behind", "being", "believe", "below", "beside", "besides", "best", "better", "between", "beyond", \
			 "both", "brief", "but", "by", "c", "c'mon", "c's", "came", "can", "can't", "cannot", "cant", "cause", "causes", "certain", "certainly", \
			 "changes", "clearly", "co", "com", "come", "comes", "concerning", "consequently", "consider", "considering", "contain", "containing", "contains", \
			 "corresponding", "could", "couldn't", "course", "currently", "d", "definitely", "described", "despite", "did", "didn't", "different", "do", "does", \
			 "doesn't", "doing", "don't", "done", "down", "downwards", "during", "e", "each", "edu", "eg", "eight", "either", "else", "elsewhere", "enough", "entirely", \
			 "especially", "et", "etc", "even", "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except", "f", "far", \
			 "few", "fifth", "first", "five", "followed", "following", "follows", "for", "former", "formerly", "forth", "four", "from", "further", "furthermore", "g", \
			 "get", "gets", "getting", "given", "gives", "go", "goes", "going", "gone", "got", "gotten", "greetings", "h", "had", "hadn't", "happens", "hardly", "has", \
			 "hasn't", "have", "haven't", "having", "he", "he's", "hello", "help", "hence", "her", "here", "here's", "hereafter", "hereby", "herein", "hereupon", "hers", \
			 "herself", "hi", "him", "himself", "his", "hither", "hopefully", "how", "howbeit", "however", "i", "i'd", "i'll", "i'm", "i've", "ie", "if", "ignored", "immediate", \
			 "in", "inasmuch", "inc", "indeed", "indicate", "indicated", "indicates", "inner", "insofar", "instead", "into", "inward", "is", "isn't", "it", "it'd", "it'll", "it's", \
			 "its", "itself", "j", "just", "k", "keep", "keeps", "kept", "know", "knows", "known", "l", "last", "lately", "later", "latter", "latterly", "least", "less", "lest", \
			 "let", "let's", "like", "liked", "likely", "little", "look", "looking", "looks", "ltd", "m", "mainly", "many", "may", "maybe", "me", "mean", "meanwhile", "merely", \
			 "might", "more", "moreover", "most", "mostly", "much", "must", "my", "myself", "n", "name", "namely", "nd", "near", "nearly", "necessary", "need", "needs", "neither", \
			 "never", "nevertheless", "new", "next", "nine", "no", "nobody", "non", "none", "noone", "nor", "normally", "not", "nothing", "novel", "now", "nowhere", "o", "obviously", \
			 "of", "off", "often", "oh", "ok", "okay", "old", "on", "once", "one", "ones", "only", "onto", "or", "other", "others", "otherwise", "ought", "our", "ours", "ourselves", \
			 "out", "outside", "over", "overall", "own", "p", "particular", "particularly", "per", "perhaps", "placed", "please", "plus", "possible", "presumably", "probably", \
			 "provides", "q", "que", "quite", "qv", "r", "rather", "rd", "re", "really", "reasonably", "regarding", "regardless", "regards", "relatively", "respectively", "right", \
			 "s", "said", "same", "saw", "say", "saying", "says", "second", "secondly", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", \
			 "sent", "serious", "seriously", "seven", "several", "shall", "she", "should", "shouldn't", "since", "six", "so", "some", "somebody", "somehow", "someone", "something", \
			 "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specified", "specify", "specifying", "still", "sub", "such", "sup", "sure", "t", "t's", "take", "taken", \
			 "tell", "tends", "th", "than", "thank", "thanks", "thanx", "that", "that's", "thats", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "there's", \
			 "thereafter", "thereby", "therefore", "therein", "theres", "thereupon", "these", "they", "they'd", "they'll", "they're", "they've", "think", "third", "this", "thorough", \
			 "thoroughly", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "took", "toward", "towards", "tried", "tries", "truly", "try", \
			 "trying", "twice", "two", "u", "un", "under", "unfortunately", "unless", "unlikely", "until", "unto", "up", "upon", "us", "use", "used", "useful", "uses", "using", \
			 "usually", "uucp", "v", "value", "various", "very", "via", "viz", "vs", "w", "want", "wants", "was", "wasn't", "way", "we", "we'd", "we'll", "we're", "we've", "welcome", \
			 "well", "went", "were", "weren't", "what", "what's", "whatever", "when", "whence", "whenever", "where", "where's", "whereafter", "whereas", "whereby", "wherein", \
			 "whereupon", "wherever", "whether", "which", "while", "whither", "who", "who's", "whoever", "whole", "whom", "whose", "why", "will", "willing", "wish", "with", "within", \
			 "without", "won't", "wonder", "would", "would", "wouldn't", "x", "y", "yes", "yet", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", \
			 "yourselves", "z", "zero"]

NOUN="n"
VERB="v"
ADV="r"
ADJ="a"

class DataExtractor:
	substitutions = [
		(r"\b(im|i'm)\b", "i am"),
		(r"\b(id|i'd)\b", "i would"),
		(r"\b(i'll)\b", "i will"),
		(r"\bbf|b/f\b", "boyfriend"),
		(r"\bgf|g/f\b", "girlfriend"),
		(r"\byoure\b", "you are"),
		(r"\b(dont|don't)\b", "do not"),
		(r"\b(didnt|didn't)\b", "did not"),
		(r"\b(wasnt|wasn't)\b", "was not"),
		(r"\b(isnt|isn't)\b", "is not"),
		(r"\b(arent|aren't)\b", "are not"),
		(r"\b(werent|weren't)\b", "were not"),
		(r"\b(havent|haven't)\b", "have not"),
		(r"\b(couldnt|couldn't)\b", "could not"),
		(r"\b(hadnt|hadn't)\b", "had not"),
		(r"\b(wouldnt|wouldn't)\b", "would not"),
		(r"\bgotta\b", "have to"),
		(r"\bgonna\b", "going to"),
		(r"\bwanna\b", "want to"),
		(r"\b(kinda|kind of)\b", ""),
		(r"\b(sorta|sort of)\b", ""),
		(r"\b(dunno|donno)\b", "do not know"),
		(r"\b(cos|coz|cus|cuz)\b", "because"),
		(r"\bfave\b", "favorite"),
		(r"\bhubby\b", "husband"),
		(r"\bheres\b", "here is"),
		(r"\btheres\b", "there is"),
		(r"\bwheres\b", "where is"),
		# Common acronyms, abbreviations and slang terms
		(r"\birl\b", "in real life"),
		(r"\biar\b", "in a relationship"),
		(r","," and "),
		# Remove fluff phrases
		(r"\b(btw|by the way)\b", ""),
		(r"\b(tbh|to be honest)\b", ""),
		(r"\b(imh?o|in my( humble)? opinion)\b", ""),
		# Default POS tagger seems to always tag "like" (and sometimes "love") as a noun - this is a bandaid fix for now
		(r"\bprefer\b", ""),
		(r"\b(like|love)\b", "prefer"),
	]

	# Skip if any of these is the *only* attribute
	skip_lone_attributes = 	[
								"fan","expert","person","advocate","customer",
							]

	skip_attributes = 		[
								"supporter","believer","gender","backer","sucker","chapter","passenger","super","water","sitter",
								"killer","stranger","monster","leather","holder","creeper","shower","member","wonder","hungover",
								"sniper","silver","beginner","lurker","loser","number","stupider","outlier",
								"door","liquor","traitor",
								"year","ear","liar",
								"rapist","racist",
								"satan","batman","veteran",
								"hypocrite","candidate",
								"everything","everyone",
							]

	include_attributes = 	[
								"geek","nerd","nurse","cook","student","consultant","mom","dad","marine","chef","sophomore","catholic",
								#"person","enthusiast","fanboy","player","advocate", # These make sense only when accompanied by at least another noun
							]

	include_attribute_endings = ("er","or","ar","ist","an","ert","ese","te","ot")
	exclude_attribute_endings = ("ing","fucker")

	skip_verbs 			= ["were","think","guess","mean"]
	skip_prepositions 	= ["that"]
	skip_adjectives		= ["sure","glad","happy","afraid","sorry","certain"]
	skip_nouns			= ["right","way"]

	grammar = r"""
	  _VP:	
	  		{<RB.*>*<V.*>+<RB.*>*}			# adverb* verb adverb* (really think / strongly suggest / look intensely)
	  _N0:
	  		{(<DT>*<JJ>*<NN.*>+(?!<POS>))+}
	  _N:
	  		{<_N0>+(<CC><_N0>)*}
	  										# determiner adjective noun(s) (a beautiful house / the strongest fighter)
	  _N_PREP_N:
	  		{<_N>((<TO>|<IN>)<_N>)+}		# to/in noun ((newcomer) to physics / (big fan) of Queen / (newbie) in gaming )
	  POSS: 
	        {<PRP\$><_N>}					# My adjective noun/s (My awesome phone)
	  ACT1:
	  		{<PRP><_VP><IN>*<_N>}			# I verb in* adjective* noun (I am a great chef / I like cute animals / I work in beautiful* New York / I live in the suburbs)
	  ACT2:
	  		{<PRP><_VP><IN>*<_N_PREP_N>}	# Above + to/in noun (I am a fan of Jaymay / I have trouble with flannel)
	"""
	chunker = RegexpParser(grammar)

	def clean_up(self, text):
		for original, rep in self.substitutions:
			text = re.sub(original, rep, text, flags=re.I)
		return text

	def normalize(self, word, tag="N"):
		kind = NOUN
		if tag.startswith("V"):
			kind = VERB
		elif tag.startswith("RB"):
			kind = ADV
		elif tag.startswith("J"):
			kind = ADJ
		return Word(word).lemmatize(kind).lower()

	def pet_animal(self, word):
		word = word.lower()
		if re.match(r"\b(dog|cat|hamster|fish|pig|snake|rat|parrot)\b", word):
			return word
		else:
			return None

	def family_member(self, word):
		word = word.lower()
		if re.match(r"\b(mom|mother|mum|mommy)\b", word):
			return "mother"
		elif re.match(r"\b(dad|father|pa|daddy)\b", word):
			return "father"
		elif re.match(r"\b(brother|sister|son|daughter)s?\b", word):
			return word
		else:
			return None

	def relationship_partner(self, word):
		word = word.lower()
		if re.match(r"\b(ex-)*(boyfriend|girlfriend|so|wife|husband)\b", word):
			return word
		else:
			return None

	def gender(self, word):
		word = word.lower()
		if re.match(r"\b(girl|woman|female|lady|she)\b", word):
			return "female"
		elif re.match(r"\b(guy|man|male|he|dude)\b", word):
			return "male"
		else:
			return None

	def orientation(self, word):
		word = word.lower()
		if re.match(r"\b(gay|straight|bi|bisexual|homosexual)\b", word):
			return word
		else:
			return None

	def process_verb_phrase(self, verb_tree):
		if verb_tree.label() != "_VP":
			return None
		verb_phrase = [(w.lower(),t) for w,t in verb_tree.leaves()]
		return verb_phrase

	def process_noun_phrase(self, noun_tree):
		if noun_tree.label() != "_N":
			return []
		if any(n in self.skip_nouns for n,t in noun_tree.leaves() if t.startswith("N")):
			return []
		noun_phrase = [(w.lower(),t) for w,t in noun_tree.leaves()]
		return noun_phrase

	def process_npn_phrase(self, npn_tree):
		if npn_tree.label() != "_N_PREP_N":
			return None
		noun_phrase = []
		prep_noun_phrase = []
		for i in range(len(npn_tree)):
			node = npn_tree[i]
			if type(node) is tuple: # we have hit the prepositions in a prep noun phrase
				w,t = node
				w=w.lower()
				prep_noun_phrase.append((w,t))
			else:
				if prep_noun_phrase:
					prep_noun_phrase += self.process_noun_phrase(node)
				else:
					noun_phrase = self.process_noun_phrase(node)
		return (noun_phrase, prep_noun_phrase)

	def process_possession(self, phrase):
		noun_phrase = []
		
		for i in range(len(phrase)):
			node = phrase[i]
			if type(node) is tuple: # word can only be pronoun
				w,t = node
				if t=="PRP$" and w.lower()!="my":
					return None
			else: # type has to be nltk.tree.Tree
				if node.label()=="_N":
					noun_phrase = self.process_noun_phrase(node)
				else: # what could this be?
					pass
		if noun_phrase:
			return {
				"kind":"possession",
				"noun_phrase":noun_phrase
				}
		else:
			return None

	def process_action(self, phrase):
		verb_phrase = []
		prepositions = []
		noun_phrase = []
		prep_noun_phrase = []

		for i in range(len(phrase)):
			node = phrase[i]
			if type(node) is tuple: # word is either pronoun or preposition
				w,t = node
				if t=="PRP" and w.lower()!="i":
					return None
				elif t=="IN":
					prepositions.append((w.lower(),t))
				else: # what could this be?!
					pass
			else:
				if node.label()=="_VP":
					verb_phrase = self.process_verb_phrase(node)
				elif node.label()=="_N":
					noun_phrase = self.process_noun_phrase(node)
				elif node.label()=="_N_PREP_N":
					noun_phrase, prep_noun_phrase = self.process_npn_phrase(node)

		if noun_phrase:
			return {
				"kind":"action",
				"verb_phrase":verb_phrase,
				"prepositions":prepositions,
				"noun_phrase":noun_phrase,
				"prep_noun_phrase":prep_noun_phrase
				}
		else:
			return None

	def extract_chunks(self, text):
		chunks = []
		sentiments = []
		text = self.clean_up(text)
		blob = TextBlob(text)

		for sentence in blob.sentences:
			sentiments.append((sentence.sentiment.polarity, sentence.sentiment.subjectivity))
			
			if not sentence.tags or not re.search(r"\b(i|my)\b",str(sentence),re.I):
				continue

			tree = self.chunker.parse(sentence.tags)

			for subtree in tree.subtrees(filter = lambda t: t.label() in ['POSS','ACT1','ACT2']):
				
				phrase = [(w.lower(),t) for w,t in subtree.leaves()]
				phrase_type = subtree.label()

				if not any(x in [("i","PRP"), ("my","PRP$")] for x in [(w,t) for w,t in phrase]) or \
				   (phrase_type in ["ACT1","ACT2"] and (any(word in self.skip_verbs for word in [w for w,t in phrase if t.startswith("V")]) or \
														any(word in self.skip_prepositions for word in [w for w,t in phrase if t=="IN"]) or \
														any(word in self.skip_adjectives for word in [w for w,t in phrase if t=="JJ"]))
														):
					continue

				if subtree.label() == "POSS":
					chunk = self.process_possession(subtree)
					if chunk:
						chunks.append(chunk)
				elif subtree.label() in ["ACT1","ACT2"]:
					chunk = self.process_action(subtree)
					if chunk:
						chunks.append(chunk)

		return (chunks, sentiments)

	def ngrams(self,text,n=2):
		return [" ".join(w) for w in TextBlob(text).ngrams(n=n)]

	def noun_phrases(self, text):
		return TextBlob(text).noun_phrases

	def common_words(self,text):
		return [word for word in list(TextBlob(text).words) if word not in stopwords and word.isalpha()]

	@staticmethod
	def test_sentence(sentence):
		print TextBlob(sentence).tags
