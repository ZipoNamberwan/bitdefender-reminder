<?php

namespace App\Http\Controllers;

use App\Models\Device;
use App\Models\Organization;
use App\Models\Status;
use Illuminate\Http\Request;
use Inertia\Inertia;

class DeviceController extends Controller
{
    public function index()
    {
        return Inertia::render('device/Index', [
            'organizations' => Organization::orderBy('short_code')->get(['id', 'short_code', 'name']),
            'statuses' => Status::orderBy('name')->get(['id', 'name']),
        ]);
    }

    public function getDevicesData(Request $request)
    {
        $records = Device::with(['organization', 'status']);
        $sortByOrganizationLongCode = false;

        if ($request->filled('organization')) {
            $organization = $request->input('organization');
            if (is_array($organization)) {
                $organizationIds = array_values(array_filter($organization, fn ($id) => $id !== '__NULL__'));
                $includeNullOrganization = in_array('__NULL__', $organization, true);

                if ($includeNullOrganization && count($organizationIds) > 0) {
                    $records->where(function ($query) use ($organizationIds) {
                        $query->whereIn('organization_id', $organizationIds)
                            ->orWhereNull('organization_id');
                    });
                } elseif ($includeNullOrganization) {
                    $records->whereNull('organization_id');
                } elseif (count($organizationIds) > 0) {
                    $records->whereIn('organization_id', $organizationIds);
                }
            } else {
                if ($organization === '__NULL__') {
                    $records->whereNull('organization_id');
                } else {
                    $records->where('organization_id', $organization);
                }
            }
        }

        if ($request->filled('status')) {
            $status = $request->input('status');
            if (is_array($status)) {
                $records->whereIn('status_id', $status);
            } else {
                $records->where('status_id', $status);
            }
        }

        if ($request->filled('bitdefender_id')) {
            $bitdefenderId = $request->input('bitdefender_id');
            if ($bitdefenderId === 'has') {
                $records->whereNotNull('id_bitdefender')->where('id_bitdefender', '!=', '');
            } elseif ($bitdefenderId === 'no') {
                $records->where(function ($query) {
                    $query->whereNull('id_bitdefender')->orWhere('id_bitdefender', '=', '');
                });
            }
        }

        if ($request->filled('last_update')) {
            $lastUpdate = $request->input('last_update');
            $cutoffDate = match ($lastUpdate) {
                'over_10_days' => now()->subDays(10),
                'over_1_month' => now()->subMonth(),
                'over_3_months' => now()->subMonths(3),
                'over_6_months' => now()->subMonths(6),
                default => null,
            };

            if ($cutoffDate !== null) {
                $records->where(function ($query) use ($cutoffDate) {
                    $query->whereNull('last_update_at')
                        ->orWhere('last_update_at', '<', $cutoffDate);
                });
            }
        }

        foreach (['device_name', 'id_bitdefender', 'nup', 'user', 'created_by'] as $field) {
            if (! $request->filled($field)) {
                continue;
            }

            $value = $request->input($field);
            $search = is_array($value) ? ($value[0] ?? null) : $value;

            if ($search !== null && $search !== '') {
                $records->where($field, 'like', '%'.$search.'%');
            }
        }

        $orderColumn = 'id';
        $orderDir = 'desc';
        $allowedSortColumns = [
            'organization_name',
            'id_bitdefender',
            'nup',
            'device_name',
            'user',
            'last_update_at',
            'created_by',
            'created_at',
            'updated_at',
        ];

        if (! empty($request->input('sortOrder')) && ! empty($request->input('sortField'))) {
            $requestedColumn = $request->input('sortField');
            if (in_array($requestedColumn, $allowedSortColumns, true)) {
                $orderColumn = $requestedColumn;
                $sortByOrganizationLongCode = $requestedColumn === 'organization_name';
            }

            $direction = $request->input('sortOrder') === 'ascend' ? 'asc' : 'desc';
            $orderDir = $direction;
        }

        $recordsTotal = $records->count();
        $start = max(0, (int) $request->input('start', 0));
        $length = (int) $request->input('length', 10);

        // Pagination
        if ($length !== -1) {
            $records->skip($start)->take($length);
        }

        // Order
        if ($sortByOrganizationLongCode) {
            $records->leftJoin('organizations', 'devices.organization_id', '=', 'organizations.id')
                ->select('devices.*')
                ->orderBy('organizations.long_code', $orderDir)
                ->orderBy('devices.id', 'desc');
        } else {
            $records->orderBy($orderColumn, $orderDir);
        }

        $data = $records->get();

        return response()->json([
            'total' => $recordsTotal,
            'data' => $data,
        ]);
    }
}
