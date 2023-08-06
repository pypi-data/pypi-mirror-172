# Noise Generator for Korean Text Grammar Error Correction Model

### This model is using python-mecab-ko as the main tokenizer.
### If you need to know the token types check the website below
### https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=aramjo&logNo=221404488280

# Requirements

## Python >= 3.7 

```consol
pip install wget
pip install konlpy
pip install hangul_utils
pip install hangul_jamo
pip install inko
pip install g2pk
pip install gensim
```
 Currently not available in Windows OS.<br />
 Only available at Linux or Colab<br />

# How to use
## Preparation
```consol
git clone https://github.com/JKJIN1999/gec_noise_generator_ko.git
```
## Manualy Download Wiki.ko.vec from this link
### https://dl.fbaipublicfiles.com/fasttext/vectors-wiki/wiki.ko.vec
### Place the wiki.ko.vec file to gec_noise_generator_ko/src/resources 

Type this in your terminal
```consol
python3 gec_noise_generator_ko/src/gecnk/noise.py --e (Error type of your preference)
```


The result will appear in results file. 


Requires a Text file with its directory as the First argument when calling the function.<br />
Text data should be in txt file and each sentence should be organized through each line.<br />

# Functions (Error Type) (second argument)

* spacing_error
> Creates Random spacing error according to rule written below<br />
> (명사, 관형어) + (명사 , 관형어 의존명사) 인 경우 띄어쓰기를 만든다<br />
> 조사와 접사를 띄어써서 생기는 오류<br />
> 단어 가운대에 띄어쓰기를 해서 생기는 오류<br />

* punctuation_error
> Converts puntuation within the same type<br />
> 문장속의 토큰중 품사가 “S-” 로 시작하는 랜덤하게 고른 토큰을 같은 품사표 내에서 랜덤하게 변경한다.<br />

* phonetic_first_error or phonetic_last_error
> Converts the first or last character if it exists in phonetic data list<br />
> 여 > 녀 / 율 > 률<br />

* remove_josa_error
> Randomly remove josa from sentence<br />
> Remove token which type starts with "J"<br />

* addition_error
> Randomly add consonant to character which has "ㅇ" as its starting consonant or doens't have the last consonant<br />
> 아기 > 바기 / 다치 > 닫치<br />

* separation_error
> From the randomly selected word, decompose the letter to consonant and vowel<br />
> 할 > ㅎㅏㄹ<br />

* typing_language_error
> Convert Korean text to English text regarding to the same keyboard position<br />
> 한글 > gksrmf / 고양이 > rhdiddl<br />

* postposition_diff_josa_error or postposition_same_josa_error
> Convert a Josa to either different or same type of Josa from the Josa dataset.<br />
> 를 > 을 / 에게 > 할<br />

* busa_error
> Convert busa "이" to "히" either way<br />
> 부단히 > 부단이 / 같이 > 같히<br />

* middle_shiot_error
> If there is "ㅅ" as the last consonant in a word longer than 2 characters, erase the last consonant "ㅅ"<br />
> 숫자 > 수자 / 찻잔 > 차잔<br />

* grapheme_to_phonem_error
> Convert the word's textual form as it is pronounciated. If the textual outcome based on the pronounciation of that specific word is not same as the current textual form of the word<br />
> 행복하다 > 행보카다 / 같이 > 가치<br />

* overlapping_sound_error
> If there are two continuous Tensed Consonant letter positioning in each first consonant letter, convert the second letter's first consonant into Basic Consonant.<br />
> 딱딱하다 > 딱닥하다 / 쌉쌀하다 > 쌉살하다<br />

* final_suffix_error
> Convert the randomly selected final suffix into a different final suffix that doesn't match the original suffix<br />
> 하겠습니다 > 하겠습네까 / 하고있다 > 하고있니<br />

* mag_error & maj_error
> By using the similarity function in Gensim KeyedVector, convert the typical pumsa type (mag or maj) into a different busa.<br />
> mag 얼마나 > 어떻게 / maj 하지만 > 그러나<br />

* polite_speech_error
> Misusage of two types of polite speech josa, nominative josa and adverbal josa<br />
> 이,가 > 께서 / 에게 > 께
