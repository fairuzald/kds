from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Bacteria(Base):
    """Database model for bacteria data."""

    __tablename__ = "bacteria"

    id = Column(Integer, primary_key=True, index=True)
    bacteria_id = Column(String(20), unique=True, index=True)
    name = Column(String(255), index=True)

    superkingdom = Column(String(100))
    kingdom = Column(String(100))
    phylum = Column(String(100))
    class_name = Column(String(100))
    order = Column(String(100))
    family = Column(String(100))
    genus = Column(String(100))
    species = Column(String(100))
    strain = Column(String(100))

    gram_stain = Column(String(50))
    shape = Column(String(100))
    mobility = Column(Boolean, default=False)
    flagellar_presence = Column(Boolean, default=False)
    number_of_membranes = Column(String(10))
    oxygen_preference = Column(String(100))
    optimal_temperature = Column(Float)
    temperature_range = Column(String(100))
    habitat = Column(String(255))
    biotic_relationship = Column(String(100))
    cell_arrangement = Column(String(255))
    sporulation = Column(Boolean, default=False)
    metabolism = Column(String(255))
    energy_source = Column(String(255))

    is_pathogen = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ScrapeLog(Base):
    __tablename__ = "scrape_logs"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)

    total_urls = Column(Integer, default=0)
    successful_scrapes = Column(Integer, default=0)
    failed_scrapes = Column(Integer, default=0)

    error_message = Column(Text)

    scraping_delay = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
