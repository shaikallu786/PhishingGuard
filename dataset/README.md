# Dataset Folder

Place your email datasets here for training the phishing detection model.

## Expected Format

The training script expects a CSV file named `emails.csv` with the following format:

```csv
text,label
"email content here",1
"another email content",0
```

Where:
- `text`: The raw email content (string)
- `label`: 
  - `1` = Phishing email
  - `0` = Legitimate email

## Example

```csv
text,label
"URGENT: Your account has been compromised! Click here to verify.",1
"Hi team, reminder about our meeting tomorrow at 10 AM.",0
```

## Notes

- If no dataset file is found, the training script uses a built-in sample dataset
- For better accuracy, use a larger dataset with diverse examples
- Consider using publicly available phishing datasets for research
