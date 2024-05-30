import pickle
from PIL import Image

from model.serialization.Jpug import Jpug

class Parser():
    '''
    Static class to load and save the Jpug objects.
    '''

    @staticmethod
    def load_image(file:str) -> Image.Image:
        '''
        Load an Image object from a file.

        Parameters:
        @param file: The file to load the object from.

        Returns:
        The Image object representing the image.
        '''
        
        return Image.open(file)

    @staticmethod
    def save_image(image:Image.Image, file:str) -> None:
        '''
        Save an image object to a file.

        Parameters:
        @param image: The image object to save.
        @param file: The file to save the object to.
        '''
        
        image.save(file)

    @staticmethod
    def load_jpug(file:str) -> Jpug:
        '''
        Load a Jpug object from a file.

        Parameters:
        @param file: The file to load the object from.

        Returns:
        The Jpug object.
        '''
        
        with open(file, 'rb') as f:
            return pickle.load(f)
        

    @staticmethod
    def save_jpug(jpug:Jpug, file:str) -> None:
        '''
        Save a Jpug object to a file.

        Parameters:
        @param jpug: The object to save.
        @param file: The file to save the object to.
        '''
        
        with open(file, 'wb') as f:
            pickle.dump(jpug, f)