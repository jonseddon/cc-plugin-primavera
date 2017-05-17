#!/usr/bin/env python
"""
compliance_checker.primavera

Compliance Test Suite for the PRIMAVERA project
"""
import os

# Import library to interact with Controlled Vocabularies
import pyessv

from compliance_checker.base import BaseCheck, BaseNCCheck, Result, TestCtx


class PrimCheck(BaseNCCheck):
    register_checker = True
    name = 'primavera'


    @classmethod
    def make_result(cls, level, score, out_of, name, messages):
        return Result(level, (score, out_of), name, messages)

    def setup(self, ds):
        self._cache_controlled_vocabularies()

    def _cache_controlled_vocabularies(self):
        """
        Loads controlled vocabularies once and caches them.
        """
        self._wcrp_cmip6_cv = pyessv.load('wcrp', 'cmip6')

    def check_global_attributes(self, ds):
        """
        Verifies the base metadata in the global attributes
        """
        attribute_fields = [
            'Conventions',
            'cake'
        ]
        level = BaseCheck.MEDIUM
        out_of = 0
        score = 0
        messages = []
        for field in attribute_fields:
            field_val = getattr(ds, field, None)
            out_of += 1
            if field_val is None:
                messages.append('%s global attribute is missing' % field)
            else:
                score += 1

            out_of += 1
            contains_string = False
            if isinstance(field_val, basestring):
                if len(field_val.strip()) > 0:
                    score += 1
                    contains_string = True
            if not contains_string:
                messages.append('%s global attribute can not be empty' % field)
        
        return self.make_result(level, score, out_of, 
                                'Required Global Attributes', messages)
                                
    def check_filename_cmpts(self, ds):
        """
        Checks that there are the correct number of components in the filename
        """
        filename_checks = TestCtx(BaseCheck.MEDIUM, 'Filename Components')
        
        filepath = ds.filepath()
        filename_checks.assert_true(filepath, 'Unable to determine filepath '
                                             'from netCDF4 library.')
                                             
        if filepath:
            filename = os.path.basename(filepath)
        else:
            filename = None
        
        filename_checks.assert_true(filename, 'Unable to determine filename'
                                             ' from netCDF4 library.')
                                             
        if filename:
            filename_cmpts = filename.strip('.nc').split('_')
            num_cmpts = len(filename_cmpts)
            # the time string is optional and so give it a bonus component
            # number if missing
            if not filename_cmpts[-1][-1].isdigit():
                num_cmpts += 1

        else:
            num_cmpts = 0
                        
        filename_checks.assert_true(num_cmpts == 7, 'Wrong number of '
            'components in filename.')

        return filename_checks.to_result()

    def check_frequency_global_attribute(self, ds):
        """
        Verifies value of the 'frequency' global attribute is
        from CMIP6 vocabulary.
        """
        term = 'frequency'

        ctx = TestCtx(category=BaseCheck.MEDIUM, description='Checks "{}" global att vs CV'.format(term))
        allowed_values = [trm.label for trm in self._wcrp_cmip6_cv[term].terms]
        gattr = ds.getncattr(term)

        test_name = 'Checks "{}" global att vs CV'.format(term)
        out_of = 2

        if not gattr:
            return self.make_result(BaseCheck.MEDIUM, 0, out_of, test_name,
                                    ['Global attribute "{}" not found.'.format(term)])

        if gattr not in allowed_values:
            return self.make_result(BaseCheck.MEDIUM, 1, out_of, test_name,
                                    ['Global attribute "{}" not in allowed values.'.format(term)])

        return self.make_result(BaseCheck.MEDIUM, 2, out_of, test_name, [])

