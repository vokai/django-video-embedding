#-*- coding: utf-8 -*-
import tempfile, io
from io import BytesIO
from django import forms
from django.core import checks
from django.db.models.fields.files import FieldFile, FileDescriptor, FileField
from django.core.files.base import File
from django.utils.translation import gettext_lazy as _
from django.db.models import signals
from django.contrib import messages
import subprocess, os
import json


codec_list = [
'264', '3g2', '3gp', '3gp2', '3gpp', '3gpp2', '3mm', '3p2', '60d', '787', '89', 'aaf', 'aec', 'aep', 'aepx',
'aet', 'aetx', 'ale', 'am', 'amc', 'amv', 'amx', 'anim', 'aqt', 'arcut', 'arf', 'asf', 'asx', 'avb',
'avc', 'avd', 'avi', 'avp', 'avs', 'avs', 'avv', 'axm', 'bdm', 'bdmv', 'bdt2', 'bdt3', 'bik', 'bin', 'bix',
'bmk', 'bnp', 'box', 'bs4', 'bsf', 'bvr', 'byu', 'camproj', 'camrec', 'camv', 'ced', 'cel', 'cine', 'cip',
'clpi', 'cmmp', 'cmmtpl', 'cmproj', 'cmrec', 'cpi', 'cst', 'cvc', 'cx3', 'd2v', 'd3v', 'dat', 'dav', 'dce',
'dck', 'dcr', 'dcr', 'ddat', 'dif', 'dir', 'divx', 'dlx', 'dmb', 'dmsd', 'dmsd3d', 'dmsm', 'dmsm3d', 'dmss',
'dmx', 'dnc', 'dpa', 'dpg', 'dream', 'dsy', 'dv', 'dv-avi', 'dv4', 'dvdmedia', 'dvr', 'dvr-ms', 'dvx', 'dxr',
'dzm', 'dzp', 'dzt', 'edl', 'evo', 'eye', 'ezt', 'f4p', 'f4v', 'fbr', 'fbr', 'fbz', 'fcp', 'fcproject',
'ffd', 'flc', 'flh', 'fli', 'flv', 'flx', 'gfp', 'gl', 'gom', 'grasp', 'gts', 'gvi', 'gvp', 'h264', 'hdmov',
'hkm', 'ifo', 'imovieproj', 'imovieproject', 'ircp', 'irf', 'ism', 'ismc', 'ismv', 'iva', 'ivf', 'ivr', 'ivs',
'izz', 'izzy', 'jss', 'jts', 'jtv', 'k3g', 'kmv', 'ktn', 'lrec', 'lsf', 'lsx', 'm15', 'm1pg', 'm1v', 'm21',
'm21', 'm2a', 'm2p', 'm2t', 'm2ts', 'm2v', 'm4e', 'm4u', 'm4v', 'm75', 'mani', 'meta', 'mgv', 'mj2',
'mk3d', 'mkv', 'mmv', 'mnv', 'mob', 'mod', 'modd', 'moff', 'moi', 'moov', 'mov', 'movie', 'mp21',
'mp21', 'mp2v', 'mp4', 'mp4v', 'mpe', 'mpeg', 'mpeg1', 'mpeg4', 'mpf', 'mpg', 'mpg2', 'mpgindex', 'mpl',
'mpl', 'mpls', 'mpsub', 'mpv', 'mpv2', 'mqv', 'msdvd', 'mse', 'msh', 'mswmm', 'mts', 'mtv', 'mvb', 'mvc',
'mvd', 'mve', 'mvex', 'mvp', 'mvp', 'mvy', 'mxf', 'mxv', 'mys', 'ncor', 'nsv', 'nut', 'nuv', 'nvc', 'ogm',
'ogg', 'ogv', 'ogx', 'osp', 'otrkey', 'pac', 'par', 'pds', 'pgi', 'photoshow', 'piv', 'pjs', 'playlist', 'plproj',
'pmf', 'pmv', 'pns', 'ppj', 'prel', 'pro', 'prproj', 'prtl', 'psb', 'psh', 'pssd', 'pva', 'pvr', 'pxv',
'qt', 'qtch', 'qtindex', 'qtl', 'qtm', 'qtz', 'r3d', 'rcd', 'rcproject', 'rdb', 'rec', 'rm', 'rmd', 'rmd',
'rmp', 'rms', 'rmv', 'rmvb', 'roq', 'rp', 'rsx', 'rts', 'rts', 'rum', 'rv', 'rvid', 'rvl', 'sbk', 'sbt',
'scc', 'scm', 'scm', 'scn', 'screenflow', 'sec', 'sedprj', 'seq', 'sfd', 'sfvidcap', 'siv', 'smi', 'smi',
'smil', 'smk', 'sml', 'smv', 'spl', 'sqz', 'srt', 'ssf', 'ssm', 'stl', 'str', 'stx', 'svi', 'swf', 'swi',
'swt', 'tda3mt', 'tdx', 'thp', 'tivo', 'tix', 'tod', 'tp', 'tp0', 'tpd', 'tpr', 'trp', 'ts', 'tsp', 'ttxt',
'tvs', 'usf', 'usm', 'vc1', 'vcpf', 'vcr', 'vcv', 'vdo', 'vdr', 'vdx', 'veg','vem', 'vep', 'vf', 'vft',
'vfw', 'vfz', 'vgz', 'vid', 'video', 'viewlet', 'viv', 'vivo', 'vlab', 'vob', 'vp3', 'vp6', 'vp7', 'vpj',
'vro', 'vs4', 'vse', 'vsp', 'w32', 'wcp', 'webm', 'wlmp', 'wm', 'wmd', 'wmmp', 'wmv', 'wmx', 'wot', 'wp3',
'wpl', 'wtv', 'wve', 'wvx', 'xej', 'xel', 'xesc', 'xfl', 'xlmv', 'xmv', 'xvid', 'y4m', 'yog', 'yuv', 'zeg',
'zm1', 'zm2', 'zm3', 'zmv'  ]


'''
    This class extends forms.FileField and evaluate if the file is a valid video format
'''
class VideoFormField(forms.FileField):
    default_error_messages = {
        'invalid_video': _(
            'Please Upload a valid video. The file you have uploaded was either not a '
            'video or a corrupted video.'
        )
    }

    def check_is_video(self, videofile_path):
        try:
            returned_data = subprocess.check_output(['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', videofile_path])                
            serialized = json.loads(returned_data)
            codec_name = serialized['format']['format_name']
            codec = codec_name.split(',')
            matching = False
            for item in codec:
                if item in codec_list:
                    matching = True
                #matching = [s for s in codec_list if item.strip(' ').lower() in s]
            if not matching:
                return False
            return True
        except subprocess.CalledProcessError as e:
            return False
    
    def to_python(self, data):
        """
        Check that the file-upload field data contains a valid image (GIF, JPG,
        PNG, etc. -- whatever Pillow supports).
        """
        f = super().to_python(data)
        if f is None:
            return None
        # We need to get a file object for Pillow. We might have a path or we might
        # have to read the data into memory.
        if hasattr(data, 'temporary_file_path'):
            file = data.temporary_file_path()
        else:
            if hasattr(data, 'read'):       
                content = data.read()
            else:
                content = data['content']

            fd, file = tempfile.mkstemp()

            with io.open(fd, 'wb') as fs:  
                fs.write(content)
        
        if not self.check_is_video(file):
            raise forms.ValidationError(
                self.error_messages['invalid_video'],
                code='invalid_video'
            )
        if hasattr(f, 'seek') and callable(f.seek):
            f.seek(0)
        return f


class VideoFile(File):
    """
    Just like the FieldFile, but for VideoFieldFiels. The only difference is
    opening the file with ffprobe and returning width and height
    """
    
    def get_dimension(self):
        videofile_path = self.file.__str__()
        returned_data = subprocess.check_output(['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', videofile_path])
        serialized = json.loads(returned_data)
        width = serialized['streams'][0]['width']
        height = serialized['streams'][0]['height']
        dimension = {'width': width, 'height': height}
        return dimension
    
    @property
    def dimension(self):
        return self.get_dimension()

class VideoFieldFile(VideoFile, FieldFile):
    def delete(self, save=True):
        # Clear the image dimensions cache
        if hasattr(self, '_dimensions_cache'):
            del self._dimensions_cache
        super().delete(save)

class VideoFileDescriptor(FileDescriptor):
    """
    Just like the FileDescriptor, but for VideoFields. The only difference is
    assigning the width/height to the width_field/height_field, if appropriate.
    """
    def __set__(self, instance, value):
        previous_file = instance.__dict__.get(self.field.name)
        super().__set__(instance, value)

        # To prevent recalculating image dimensions when we are instantiating
        # an object from the database (bug #11084), only update dimensions if
        # the field had a value before this assignment.  Since the default
        # value for FileField subclasses is an instance of field.attr_class,
        # previous_file will only be None when we are called from
        # Model.__init__().  The ImageField.update_dimension_fields method
        # hooked up to the post_init signal handles the Model.__init__() cases.
        # Assignment happening outside of Model.__init__() will trigger the
        # update right here.
        if previous_file is not None:
            self.field.update_dimension_fields(instance, force=True)
            
class VideoField(FileField):
    attr_class = VideoFieldFile
    descriptor_class = VideoFileDescriptor
    description = _("Video")
    
    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, **kwargs):
        self.width_field, self.height_field = width_field, height_field
        super().__init__(verbose_name, name, **kwargs)

    def check(self, **kwargs):
        return [
            *super().check(**kwargs),
            *self._check_ffprobe_installed(),
        ]

    def _check_ffprobe_installed(self):
        FNULL = open(os.devnull, 'w')
        exit_code = subprocess.call(['which', 'ffprobe'], stdout=FNULL,  stderr=subprocess.STDOUT)

        if not exit_code == 0:
            return [
                checks.Error(
                    'Cannot use VideoField because ffprobe is not installed.',
                    hint='Get ffmpeg at https://ffmpeg.org/download.html',
                    obj=self,
                    id='videofield.E001',
                )
            ]

        return []

    def get_absolute_video_name(self):
        return True

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.width_field:
            kwargs['width_field'] = self.width_field
        if self.height_field:
            kwargs['height_field'] = self.height_field
        return name, path, args, kwargs

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        # Attach update_dimension_fields so that dimension fields declared
        # after their corresponding image field don't stay cleared by
        # Model.__init__, see bug #11196.
        # Only run post-initialization dimension update on non-abstract models
        if not cls._meta.abstract:
            signals.post_init.connect(self.update_dimension_fields, sender=cls)

    def update_dimension_fields(self, instance, force=False, *args, **kwargs):
        """
        Update field's width and height fields, if defined.

        This method is hooked up to model's post_init signal to update
        dimensions after instantiating a model instance.  However, dimensions
        won't be updated if the dimensions fields are already populated.  This
        avoids unnecessary recalculation when loading an object from the
        database.

        Dimensions can be forced to update with force=True, which is how
        ImageFileDescriptor.__set__ calls this method.
        """
        # Nothing to update if the field doesn't have dimension fields or if
        # the field is deferred.
        has_dimension_fields = self.width_field or self.height_field
        if not has_dimension_fields or self.attname not in instance.__dict__:
            return

        # getattr will call the VideoFileDescriptor's __get__ method, which
        # coerces the assigned value into an instance of self.attr_class
        # (ImageFieldFile in this case).
        file = getattr(instance, self.attname)

        # Nothing to update if we have no file and not being forced to update.
        if not file and not force:
            return

        dimension_fields_filled = not(
            (self.width_field and not getattr(instance, self.width_field)) or
            (self.height_field and not getattr(instance, self.height_field))
        )
        # When both dimension fields have values, we are most likely loading
        # data from the database or updating an image field that already had
        # an image stored.  In the first case, we don't want to update the
        # dimension fields because we are already getting their values from the
        # database.  In the second case, we do want to update the dimensions
        # fields and will skip this return because force will be True since we
        # were called from ImageFileDescriptor.__set__.
        if dimension_fields_filled and not force:
            return

        # file should be an instance of ImageFieldFile or should be None.
        if file:
            width = file.width
            height = file.height
        else:
            # No file, so clear dimensions fields.
            width = None
            height = None

        # Update the width and height fields.
        if self.width_field:
            setattr(instance, self.width_field, width)
        if self.height_field:
            setattr(instance, self.height_field, height)

    def formfield(self, **kwargs):
        return super().formfield(**{
            'form_class': VideoFormField,
            **kwargs,
        })
