# Notes WhisperPI

## Maximum Prompt Tokens

We know from this [comment](https://github.com/openai/whisper/discussions/117#discussioncomment-5350408) that the last 223 (`model.dims.n_text_ctx // 2 - 1`) tokens of the given prompt will be used for transcription. If there are less than 223 tokens in the prompt, context tokens will be passed in as well up to the 223 token mark.

The line of code where this cutoff is implemented is [here](https://github.com/rmohl/whisper/blob/main/pi_whisper/decoding.py#L599)

We know from this [OpenAI website](https://platform.openai.com/tokenizer) that approximately every 4 characters of text is equivalent to a single token. This means that the max prompt for WhisperPI is about 4 * 223 = 892 characters (note that commas and spaces also count).

## Next Steps 

### Other Transcription Variables

- prefix
- sample_len (affects prefix length)
- best_of
- beam_size
- patience 
- temperature

### Altering Prompt Options

- reversing order of prompt so that first words/phrases provided are ensured to be included
- changing maximum prompt tokens allowed before cutoff
