<?php

namespace App\Http\Controllers;

use App\Models\Device;
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Inertia\Inertia;

class DeviceController extends Controller
{
    public function index()
    {
        return Inertia::render('device/Index');
    }

    public function getDevicesData(Request $request)
    {
        $user = User::find(Auth::id());

        $records = Device::with(['organization', 'status']);

        if ($request->input('organization')) {
            $records->where('organization_id', $request->input('organization'));
        }

        $orderColumn = 'created_at';
        $orderDir = 'desc';

        if (!empty($request->input('sortOrder')) && ! empty($request->input('sortField'))) {
            $orderColumn = $request->input('sortField');
            $direction = $request->input('sortOrder') === 'ascend' ? 'asc' : 'desc';
            $orderDir = $direction;
        }

        $recordsTotal = $records->count();

        // Pagination
        if ($request->input('length') != -1) {
            $records->skip($request->input('start'))
                ->take($request->input('length'));
        }

        // Order
        $records->orderBy($orderColumn, $orderDir);

        $data = $records->get();

        return response()->json([
            'total' => $recordsTotal,
            'data' => $data,
        ]);
    }
}
