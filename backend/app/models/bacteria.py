from datetime import datetime

from app.db.session import Base
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text


class Bacteria(Base):
    __tablename__ = "bacteria"

    id = Column(Integer, primary_key=True, index=True)
    bacteria_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(255), index=True)
    superkingdom = Column(String(100), nullable=True)
    kingdom = Column(String(100), nullable=True)
    phylum = Column(String(100), nullable=True)
    class_name = Column(String(100), nullable=True)
    order = Column(String(100), nullable=True)
    family = Column(String(100), nullable=True)
    genus = Column(String(100), nullable=True)
    species = Column(String(100), nullable=True)
    strain = Column(String(255), nullable=True)
    gram_stain = Column(String(50), nullable=True)
    shape = Column(String(100), nullable=True)
    mobility = Column(Boolean, nullable=True)
    flagellar_presence = Column(Boolean, nullable=True)
    number_of_membranes = Column(String(50), nullable=True)
    oxygen_preference = Column(String(100), nullable=True)
    optimal_temperature = Column(Float, nullable=True)
    temperature_range = Column(String(100), nullable=True)
    habitat = Column(String(500), nullable=True)
    biotic_relationship = Column(String(255), nullable=True)
    cell_arrangement = Column(String(255), nullable=True)
    sporulation = Column(Boolean, nullable=True)
    metabolism = Column(String(500), nullable=True)
    energy_source = Column(String(255), nullable=True)
    is_pathogen = Column(Boolean, default=False, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Bacteria(bacteria_id='{self.bacteria_id}', name='{self.name}')>"


class ScrapeLog(Base):
    __tablename__ = "scrape_logs"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    total_urls_processed = Column(Integer, default=0)
    successful_scrapes = Column(Integer, default=0)
    failed_scrapes = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    source = Column(String(100), default="mimedb_live")
    created_at = Column(DateTime, default=datetime.utcnow)
