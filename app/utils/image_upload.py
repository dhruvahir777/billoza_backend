import os
import shutil
from fastapi import UploadFile, HTTPException
from pathlib import Path
from app.core.config import settings
import uuid

async def save_upload_file(upload_file: UploadFile, folder: str = "profile") -> str:
    """
    Save an uploaded file to disk.
    
    Args:
        upload_file: The file to save
        folder: The subfolder to save in (e.g., 'profile', 'menu')
        
    Returns:
        str: The path to the saved file
    """
    # Ensure the upload directory exists
    upload_dir = Path(settings.UPLOAD_DIR) / folder
    os.makedirs(upload_dir, exist_ok=True)
    
    # Get file content
    content = await upload_file.read()
    
    # Check file size
    if len(content) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=413, detail="File too large")
    
    # Generate a unique filename
    file_extension = os.path.splitext(upload_file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = upload_dir / unique_filename
    
    # Write the file
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Return the relative path to be stored in the database
    return str(Path(folder) / unique_filename)

def delete_file(file_path: str) -> bool:
    """
    Delete a file from disk.
    
    Args:
        file_path: The path to the file to delete
        
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    try:
        # Join with the upload dir
        full_path = Path(settings.UPLOAD_DIR) / file_path
        
        # Check if file exists
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
        return False
    except Exception:
        return False
