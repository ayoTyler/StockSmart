# <span style="color: limegreen;">Micro Center Stock Application (MCSA) v1.0.1</span>

###### <i>Licensed with Apache 2.0 - Check the <b>LICENSE</b> file in the main branch for more information</i>

Check the stock of a specific Micro Center product. Optionally, securely link your email to get notified when your selected product is in stock.

## <span style="color: limegreen;">Installation</span>

<i>**Note: The default code checks the Micro Center Stores in Dallas, TX and Houston, TX</i>


<b>Step-by-step instructions for setting up the project:</b>
    <br>
1.  <b>Clone the repository:</b>
    ```bash
    git clone https://github.com/ayoTyler/Micro-Center-Stock-Application.git
    ```
    *Alternatively: If you choose to download the <b>.zip</b> from GitHub:<br>
    1\. Extract the files to a folder using <i>7zip</i> or <i>WinRAR</i> <br>
    2\. Open the <b>MCSA.py</b> application in a Python-supported IDE. (I recommend <i>PyCharm Community Edition</i>) <br>
    <br>
2.  <b>Open the command console/terminal window within your IDE. Change directory (cd) to the project folder's location (if needed) and run the following:</b>
    ```bash
    pip install -r requirements.txt
    ```
    *Alternatively: To use your system's command console/terminal window to install the items listed within the requirements folder:<br>
    1\. Change directory (`cd`) to the project folder's location that contains <b>requirements.txt</b> <br>
    2\. Run the above command<br>
    <br>
3.  <b>On Line 232 within the code, replace the store names with the name of your local Micro Center store(s):</b>
    ```python
    # Line 232
    stores_to_check = ['Dallas']
    ```

    <br>
4.  <b>On Line 47 within the code, add or update the Product Page URL with your desired product:</b>
    ```python
    # Line 47 - Get the product page URL
    PRODUCTS = {
        'simple-part-name-here': 'https://www.microcenter.com/your-product-url-here',
    }
    ```
    <br>
5.  <b><i>(Optional)</i> Adjust the speed that the program functions:</b>
    <br>
    <br>
    Slower Internet = Higher Number (~30)
    ```python
    # Line 122, 143, 160, 249, 252 - Wait for the page to load,
    # adjust as needed (seconds)
    time.sleep(30)
    ```
    
    <br>
    
    Faster Internet = Lower Number (~5)
    ```python
    # Line 122, 143, 160, 249, 252 - Wait for the page to load,
    # adjust as needed (seconds)
    time.sleep(5)
    ```
    
    <br>
    It is <u>NOT</u> recommended to set the number below 5.
    <br>
    <br>
6.  <b><i>(Optional)</i> When you run the program, follow the instructions in the terminal/run console to securely connect your email to the application.</b><br>
    <br>
    When linked, this application sends you an alert email when your desired product is in stock. Otherwise, the program will run normally and notify you via the terminal/run console.<br>
    <br>
    <b>To securely link your email, follow the instructions in the terminal/run console or the instructions below:</b><br>
    1\. Go to myaccount.google.com<br>
    2\. Search 'App Passwords' and click the respective option<br>
    3\. In the 'App name' field, enter any title specific to this program<br>
    4\. Copy and paste the newly generated password into the appropriate fields given to you in the terminal/run console<br>
    5\. Enter your email<br> 
    6\. Enter your password<br>
    7\. Expect to receive a test email from yourself confirming that your email is linked with the application<br>
    8\. To avoid having to re-enter your email and app password every time, it is recommended to place them in `./venv/config.env`. See `config.env.example` for reference.

<span style="color: limegreen;"><b><u>That's all!</u></span> Leave the program running in the background. If you shut down the computer, be sure to run through the steps again to get it working again. </b>

### <span style="color: goldenrod;">Future Update Plans</span>

1.  GUI window<br>
2.  Multiple Micro Center stores listed - no code-changing required<br>
3.  Works for other websites<br>


### <span style="color: darkturquoise;">If this program helped you, buy me a coffee :)</span><br>

https://buymeacoffee.com/ayotyler     < - - - - - - - - - - - - - - - - - 
<br>
<br>