ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf', 'xls', 'xlsx', 'csv'}


class FileValidation:

    def allowed_file(file):
        filename = file.filename
        return filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
