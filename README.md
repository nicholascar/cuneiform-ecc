![](images/cuneiform.jpg)

# Cuneiform Error Correction Coding

#### A character persistence problem
One of the problems with ancient clay tablets is that characters impressed 
into them with a reed stylus become obscured due to tablet damage.

To enhance tablet text resilience, methods known as *error correction coding*
can be employed. These add redundancy to the tablet content which then, with 
simple algorithms, can be used to fill in a certain amount of missing 
characters.

Tablets made in this way would better preserve information than those from
Ancient Sumeria have - a mere ~5,000 years to date.

#### Error correction codes 
Error correction coding is used for modern media that can suffer physical 
damage, such as compact disks. It's also used for transmitted messages in 
cases where retransmission of broken messages is unfeasible for some reason,
for example very long message travel time, as is the case with interplanetary 
probe missions.
 
Error correction codes are more efficient than simply making two copies: modern
codes require less than 25% more characters than the original message. Simple 
scheme, such as the one here, require 50% more. Also, the correction code is
*within* the message, as opposed to being something independent which must then
be kept in association with the original for message recovery.


## Demonstration

This demonstration encodes limited English into cuneiform and caters for a certain 
level of character loss: no more than 1 in 3 characters and no more than 2 in a row.

The [main.py](main.py) file is a [Python](https://en.wikipedia.org/wiki/Python_(programming_language)) 
software script which takes, as input, limited English prose (only letters,
',' & '.') and firstly produces error correction-encoded cuneiform, optionally with
a number of characters obscured to test message recovery, formatted to a fixed character 
with to allow for good tablet calligraphy on rectangular tablets.

It does this in 4 main steps:

1. **Encoding**
    - English prose has its punctuation removed, including space, and all characters
    are moved to upper case.
    - If the length of characters in the text us odd, '_' is added at the end to make
    an even-length text for pair encoding
    - For every 2 upper-case characters, an error correction character is calculated
    and inserted after the pair
2. **Transliteration**
    - English upper case letters, both original text and error correction characters,
    are transliterated into simple cuneiform characters
3. **Random obsuration**
    - A random number of characters - no more than 1/3 of the input text, no more than
    one in any original pair + correction character triplet - are obscured, that is
    the cuneiform characters are replaced with '-' indicating a lost character
4. **Tablet printing**
    - The resultant cuneiform characters are printed in lines with *n* characters per 
    line where the user specifies *n*.
    - The final line is centre space-filled with blanks (as per cuneiform norms) if 
    the message doesn't neatly divide into *n* characters  
    

### Error correction calculation
This code uses a very simple [finite field arithmetic](https://en.wikipedia.org/wiki/Finite_field_arithmetic)
(Galois field) to calculate a redundant correction character for every character 
pair. 

This is done by assigning every character from A - Z and '_' (used only to make 
input text of even character length for effective pairing of letters) a number
and then adding each pair of characters to produce a sum number which indicates
a redundant character to be added.

For example, if the characters `S` & `T` are input, their values are 18 & 19
respectively so that the sum is `18 + 19 = 37`. The finite field used is 0 - 26
(for A - z + '_') so that 37 'wraps around' becoming `37 - 27 = 10` which 
indicates `K` so we get he sequence `STK`.

Now, if `S` were to be accidentally erased from the sequence (as would happen
due to clay tablet damage), we can recalculate it by simply using the equation:

```
x + 19 = 27 + 10
```
Since we know `T` is 19, `K` is 10 and the finite field is 27.

Solving this is:

```
x = 27 + 10 - 19
  = 37 - 19
  = 18
  = S
```

### Transiteration
 



```
𒉽𒃵𒀽𒍞𒉽-𒑉𒁹-𒁹
𒁹𒑊-𒑊𒈦𒀹-𒈫𒉽𒁹
𒁹-𒈫𒈫𒀸𒐀𒈫𒀹𒈫𒑋
𒋡𒑉-𒁹𒀹--𒄑𒈫𒀸
𒐀𒀸𒆳𒁹𒁹𒁹-𒑈𒃰𒀹
𒁇-𒋡𒈫𒑋-𒆳𒆳-𒀹
𒐺𒁇𒑋𒈦𒐁𒈦𒄑𒀹𒑉-
𒈦𒀸-𒍞𒀸-𒃵𒐉𒇹𒑈
𒑊𒆳-𒃵-𒀸𒉽𒑋-𒍞
-𒉽𒑉𒍞𒁹𒁹-𒑈𒋡𒀸
𒑉𒃵-𒁹𒈫𒑊𒀸𒈫𒈫-
𒈫𒑋𒋡𒑉𒈫𒀸𒐀𒋰𒁹𒐉
-𒈫𒈫𒉽-𒀹𒁹𒈫-𒀸
𒁹𒄑-𒐁. . 𒀹𒈦𒃰𒆳
```