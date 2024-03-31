from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField


class ImageForm(FlaskForm):
    image = FileField('Image for background removing', validators=[
        FileRequired()#,
        #FileAllowed(UploadSet('images', IMAGES))
    ])
    submit = SubmitField('Submit')
