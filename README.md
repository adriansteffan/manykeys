# ManyKeys: Confidential & Centralized Data Collection for Collaborative Online Studies

ManyKeys enables labs to conduct collaborative online studies in a centralized way without exposing the content of their participant data to whoever stores it during collection. By leveraging asymmetrical encryption, ManyKeys ensures that participant data is only decipherable by the lab that the specific participant belongs to.

### Why would I need this?
In collaborative studies, data protection guidelines often forbid labs to store sensitive participant data (such as video recordings) on servers of third parties (such as collaborating labs hosting online studies). Labs often have to install separate instances of the online study software or get new ethics approvals, which is time- and resource-intensive. ManyKeys enables third parties to transmit and store data in a way that ensures the confidentiality of any participant data.

## Example Workflow
The general workflow looks as follows:

1. Participating labs each choose a **username** and **password** and use the `manykeys.py` script to derive a public keystring, which contains the username and a key used for asymmetrical encryption.

2. The centralized (open-sourced) web-frontend gets supplied the keystring (e.g. via GET parameter) and uses the methods implemented in `manykeys.js` to encrypt the data on the participant's device before transmitting it to a centralized data storage.

4. After data collection concludes, the centralized entity uses the usernames to identify labs and sends them their encrypted data.

3. The participating labs receive their data and can use the `manykeys.py` script along with their username and password to decrypt the data. Only then are the contents of the data viewable and can be used for further processing.


## Prerequisites

For both usage and development, you will need a [Python3](https://www.python.org/downloads/) installation. You will also need to run 
```
pip3 install -r requirements.txt
``` 
in the root directory after cloning the repository.


## Usage Instructions

### Generate Public Keystring
To generate your public keystring, run the python script without any arguments:

```
python3 manykeys.py
```

The script will display instructions and prompt you to choose your username and password. Your public keystring will be printed and saved to `keystring.txt`. Note that the username and password need to be remembered to restore data! There is no option to restore a lost password.

### Decrypt Files
To decrypt files that have been encrypted with the public keystring, supply the directory containing the `.enc` files as an argument :

```
python3 manykeys.py PATH_TO_DIRECTORY
```

The script will prompt you for your username and password and decrypt the files afterward. The resulting files will be saved in a folder called `decrypted`. 


## Including ManyKeys in your project

TODO


## Roadmap/Todos

* Package code for the releases page
* Documentation for including the js in frontends
* minified version of the js library
* GUI for using the python script


## Authors

- **Adrian Steffan** [adriansteffan](https://github.com/adriansteffan) [website](https://adriansteffan.com/)
* **Till Müller** - [TillMueller](https://github.com/TillMueller) - helping with the implementation of the crypto scheme and (most importantly) coming up with the name


## License

This project is licensed under the [GNU GPLv3](LICENSE.md) - see the [LICENSE.md](LICENSE.md) file for
details


