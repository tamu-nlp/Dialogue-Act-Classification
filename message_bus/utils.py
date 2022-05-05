
class Utils:

    # copy a dictionary field that may not exist
    def update_field(self, src, dst, key):
        if(key in src):
            value = src[key]
            if(value != None):
                dst.update({key:value})
