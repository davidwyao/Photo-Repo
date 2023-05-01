# PhotoRepo
### A command-line image repository program!

#### Supports:
<ul>
	<li> Bulk uploading, downloading, and deletion of image files </li>
	<li> Public images discoverable and downloadable by other users </li>
	<li> Private images discoverable and downloadable only by you </li>
</ul>

## Requirements
### Python 3
This program was tested using Python 3.9.5.
### Pyrebase
Install via terminal:
`pip install pyrebase`

## Usage
To run: `python src/main.py`

Place images you would like to upload in the `/upload` folder.
Images will be downloaded to `/download`.

Except during login, users are referred to by the part of their email before the `@`, i.e. `pytest` for `pytest@pytest.com`.

`uploadpath` and `downloadpath` parameters can be changed in [firebase_controller.py](https://github.com/davidwyao/Photo-Repo/blob/main/src/firebase_controller.py).

To run unit tests ensure `pytest.jpg` has not been deleted from `/upload`, and that `uploadpath` and `downloadpath` are at default values.

## Technologies
### Firebase via the [Pyrebase](https://github.com/thisbejim/Pyrebase) wrapper
<ul>
	<li> User authentication via email and password </li>
	<li> NoSQL database with advanced security rules </li>
	<li> Cloud storage with configurable access restrictions </li>
</ul>

### Python
<ul>
	<li> Everything else! </li>
</ul>
</ul>

## Potential additions
<ul>
	<li> Private image encryption prior to uploading using symmetric keys. </li>
</ul>
